import { Toolbar } from '@/components';

const Header = () => {
	return (
		<div className='absolute top-0 left-0 z-10 p-4'>
			<h1 className='text-2xl font-bold font-mono text-white'>🇨🇦 Canadian Spacecraft Tracker</h1>
			<p className='mt-1 text-sm font-mono text-neutral-200'>Click on satellites for details</p>
			<Toolbar />
		</div>
	);
};

export { Header };
