import type { SatelliteData } from '@/types';
import { useSatelliteStore } from '@/stores';

interface SatelliteStatsProps {
	satellite: SatelliteData | null;
}

const SatelliteStats = ({ satellite }: SatelliteStatsProps) => {
	const { followSatellite, setFollowSatellite } = useSatelliteStore();

	if (!satellite) return null;

	const toggleFollow = () => {
		// Toggle follow; if turning on but satellite lacks noradId, do nothing
		if (!followSatellite && !satellite.noradId) return;
		setFollowSatellite(!followSatellite);
	};

	return (
		<div className='z-10 absolute top-88 right-4 p-4 rounded-lg bg-neutral-200/20 backdrop-blur-md'>
			<div className='flex items-start justify-between gap-4'>
				<h2 className='font-bold font-mono text-lg text-white'>{satellite.name}</h2>
				<button type='button' onClick={toggleFollow} className={`select-none px-3 py-1 rounded text-sm font-mono ${followSatellite ? 'bg-green-600 text-white' : 'bg-neutral-800 text-neutral-200'} ${!satellite.noradId ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}>
					{followSatellite ? 'Following' : 'Follow'}
				</button>
			</div>

			<p className='mt-2 font-mono text-sm text-neutral-200'>
				<strong>Operator:</strong> {satellite.operator}
			</p>
			<p className='mt-1 font-mono text-sm text-neutral-200'>
				<strong>Launched:</strong> {satellite.launched}
			</p>
			<p className='mt-1 font-mono text-sm text-neutral-200'>
				<strong>Status:</strong> {satellite.status}
			</p>
			<p className='mt-1 font-mono text-sm text-neutral-200'>
				<strong>Altitude:</strong> {satellite.altitude} km
			</p>
			<p className='mt-1 font-mono text-sm text-neutral-200'>
				<strong>Inclination:</strong> {satellite.inclination}°
			</p>
		</div>
	);
};

export { SatelliteStats };
