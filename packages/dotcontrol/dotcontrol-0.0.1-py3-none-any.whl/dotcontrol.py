__version__ = '0.0.1'


from pathlib import Path
import shutil
import hashlib
import os.path
import toml
import click


HOME_PATH = Path.home()
DEFAULT_CONFIG = {
	'profile': 'default'
}


def mkdir_recursive(dest):
	if not dest.exists():
		for path in reversed(dest.parents):
			if not path.exists():
				path.mkdir()
		dest.mkdir()


def file_digest(bytes):
	return hashlib.sha1(bytes).hexdigest()


def relative_to_home(path):
	return os.path.relpath(path, HOME_PATH)


class BaseDot:
	@classmethod
	def resolve_paths(cls, profile, path):
		origin_path = absolute_origin_path = dot_path = None
		if path[:2] in ('~/', '~\\'):
			origin_path = Path(path)
			absolute_origin_path = origin_path.expanduser()
			dot_path = profile.dot_home_path.joinpath(path[2:])
		else:
			origin_path = Path(path).resolve()
			absolute_origin_path = Path(origin_path)
			if HOME_PATH in origin_path.parents:
				relative = origin_path.relative_to(HOME_PATH)
				origin_path = Path('~').joinpath(relative)
				dot_path = profile.dot_home_path.joinpath(relative)
			else:
				path_str = str(origin_path)
				# for Windows' sake.
				if path_str[1:3] in (':/', ':\\'):
					dot_path = profile.dot_root_path.joinpath(path_str[0] + path_str[2:])
				else:
					dot_path = profile.dot_root_path.joinpath(path_str)
		return {
			'origin_path': origin_path,
			'absolute_origin_path': absolute_origin_path,
			'dot_path': dot_path
		}

	def __init__(self, profile, path):
		self.profile = profile

		if type(path) is dict:
			self.__dict__.update(path)
		elif type(path) is str:
			self.__dict__.update(self.resolve_paths(profile, path))
		
		if not self.dot_path.exists():
			from .util import mkdir_recursive
			mkdir_recursive(self.dot_path.parent)
		

class FileDot(BaseDot):
	def update(self):
		shutil.copyfile(self.absolute_origin_path, self.dot_path)
	
	def restore(self):
		shutil.copyfile(self.dot_path, self.absolute_origin_path)
	
	def delete(self):
		if self.dot_path.exists():
			self.dot_path.unlink()
		
	def digest(self, which='dot'):
		if which == 'dot':
			which = self.dot_path
		elif which == 'origin':
			which = self.absolute_origin_path
		return file_digest(which.read_bytes())


class DirDot(BaseDot):
	def update(self):
		if self.dot_path.exists():
			self.dot_path.rmdir()
		shutil.copytree(self.absolute_origin_path, self.dot_path)

	def restore(self):
		if self.dot_path.exists():
			self.absolute_origin_path.rmdir()
			shutil.copytree(self.dot_parent, self.absolute_origin_path)
	
	def delete(self):
		if self.dot_path.exists():
			shutil.rmtree(self.dot_path)
	
	def files(self, which='dot'):
		if which == 'dot':
			which = self.dot_path
		elif which == 'origin':
			which = self.absolute_origin_path
		files = []
		dirs = [which]
		while dirs:
			for file in dirs.pop(0).iterdir():
				if file.is_dir():
					dirs.append(file)
				else:
					files.append(file)
		return files
	
	def digest(self, which='dot'):
		return {
			str(path): file_digest(path.read_bytes())for path in self.files(which)
		}


class Dot:
	def __new__(cls, profile, path):
		paths = BaseDot.resolve_paths(profile, path)
		absolute_origin_path = Path(paths['absolute_origin_path'])
		if absolute_origin_path.is_file():
			dot = FileDot(profile, path)
		elif absolute_origin_path.is_dir():
			dot = DirDot(profile, path)
		return dot


class Profile(dict):
	def __init__(self, control, name):
		self.control, self.name = control, name
		self.root_path = control.profiles_path.joinpath(name)
		self.config_path = control.profiles_path.joinpath('{}.toml'.format(name))
		self.dot_root_path = self.root_path.joinpath('root')
		self.dot_home_path = self.root_path.joinpath('home')
		self.stash_path = control.root_path.joinpath('stashes').joinpath(name)
		try:
			self.load()
		except FileNotFoundError:
			self.init()
	
	def init(self):
		if not self.root_path.exists():
			self.root_path.mkdir()
			self.dot_root_path.mkdir()
			self.dot_home_path.mkdir()
		if not self.stash_path.exists():
			self.stash_path.mkdir()

		self['digests'] = {}
		self.save()

	def load(self):
		self.update(toml.loads(self.config_path.read_text()))
	
	def save(self):
		self.config_path.write_text(toml.dumps(dict(self)))
	
	def delete(self):
		import shutil
		shutil.rmtree(self.root_path)
		self.config_path.unlink()

	def set_dot(self, path):
		dot = Dot(self, path)
		origin_digest = dot.digest('origin')
		if dot.dot_path.exists() and dot.digest('dot') == origin_digest:
			return
		
		dot.update()
		self['digests'][str(dot.origin_path)] = origin_digest
		self.save()

	def delete_dot(self, path):
		dot = Dot(self, path)
		dot.delete()
		self['digests'].pop(str(dot.origin_path), None)
		self.save()

	def activate(self):
		for path in self['digests'].keys():
			Dot(self, path).restore()

	def deactivate(self):
		pass # TODO: should dots be updated without user instruction?

	def stash(self):
		for path in self['digests'].keys():
			pass
	
	def unstash(self):
		for path in self['digests'].keys():
			pass


class DotControl:
	def __init__(self):
		self.root_path = HOME_PATH.joinpath('.config/dotcontrol')
		self.config_path = self.root_path.joinpath('config.toml')
		self.profiles_path = self.root_path.joinpath('profiles')
		
		try:
			self.load_config()
			self.current_profile = Profile(self, self.config['profile'])
		except FileNotFoundError:
			self.init()
	
	def init(self):
		from .util import mkdir_recursive
		from .const import DEFAULT_CONFIG
		
		mkdir_recursive(self.profiles_path)
		mkdir_recursive(self.root_path.joinpath('stashes'))
		self.config = DEFAULT_CONFIG
		self.current_profile = Profile(self, 'default')
		self.save_config()
	
	def init_vcs(self, vcs):
		pass

	def load_config(self):
		self.config = toml.loads(self.config_path.read_text())
	
	def save_config(self):
		self.config_path.write_text(toml.dumps(self.config))

	@property
	def all_profiles(self):
		return {
			name: Profile(self, name) for name in [path.name.replace('.toml', '') for path in self.profiles_path.iterdir() if path.name.endswith('.toml')]
		}

	def switch_profile(self, name):
		self.current_profile.deactivate()
		self.current_profile = Profile(self, name)
		self.current_profile.activate()
		self.config['profile'] = name
		self.save_config()

	def delete_profile(self, name):
		Profile(self, name).delete()
	
	def set_dot(self, path):
		self.current_profile.set_dot(path)
	
	def delete_dot(self, path):
		self.current_profile.delete_dot(path)


control = DotControl()


@click.group()
def cli():
	pass


@cli.command('ls', help='List dots in specified profiles')
@click.option('-p', '--profiles-to-list', default=None, help='Profiles to list dots of')
@click.option('--all', is_flag=True, help='List dots in all profiles')
def list_dots(profiles_to_list, all):
	if profiles_to_list:
		profiles_to_list = map(lambda x: Profile(control, x, profiles_to_list))
	else:
		if all:
			profiles_to_list = control.all_profiles.values()
		else:
			profiles_to_list = [control.current_profile]
	for profile in profiles_to_list:
		print('profile:', profile.name)
		if len(profile['digests'].keys()) is 0:
			print('no dots in this profile yet.')
			continue
		for path in profile['digests']:
			print(path)


@cli.command('add', help='Add dot(s) to current profile')
@click.argument('path', required=True, nargs=-1)
def set_dots(path):
	for path in path:
		control.set_dot(path)


@cli.command('rm', help='Delete specified dot(s) from current profile')
@click.argument('path', required=True, nargs=-1)
def delete_dots(path):
	for path in path:
		control.delete_dot(path)


@cli.command('use', help='Switch profile')
@click.argument('profile_name')
def switch_profile(profile_name):
	if not control.profiles_path.joinpath(profile_name).exists():
		print('creating profile...')
	control.switch_profile(profile_name)
	print('switched to profile', profile_name)


@cli.command('lsp', help='List profiles')
def list_profiles():
	for path in control.profiles_path.iterdir():
		if path.suffix == '.toml':
			if path.stem == control.current_profile.name:
				print('*', path.stem)
			else:
				print(path.stem)


@cli.command('rmp', help='Delete specified profile(s)')
@click.argument('profile_names', required=True, nargs=-1)
def delete_profiles(profile_names):
	for name in profile_names:
		print('deleting profile', name)
		if name == control.current_profile.name:
			print('profile', name, 'is currently in use, skipping')
			continue
		Profile(control, name).delete()

