import { Map, MapPin, RefreshCcw } from 'lucide-react';
import { useEffect, useState } from 'react';
import { type ErrorType } from '@/types';
import { useSatelliteStore } from '@/stores';
import { ErrorModal, LocationsModal } from '@/components';

const Toolbar = () => {
	const { flyToLocation } = useSatelliteStore();

	const [isLocationsModalOpen, setIsLocationsModalOpen] = useState<boolean>(false);
	const [isErrorModalOpen, setIsErrorModalOpen] = useState<boolean>(false);
	const [error, setError] = useState<ErrorType | null>(null);

	const handleRefreshTLE = () => {
		// TODO: Implement TLE data refresh logic
		// For now, just log to console
		console.log('Refreshing TLE data...');
	};

	const handleFlyToMyLocation = () => {
		if (!navigator.geolocation) {
			setError({
				title: 'Location Not Supported',
				message: 'Your browser does not support geolocation.',
			});
			setIsErrorModalOpen(true);
			return;
		}

		navigator.geolocation.getCurrentPosition(
			(position) => {
				flyToLocation(position.coords.latitude, position.coords.longitude);
			},
			(error) => {
				setError({
					title: 'Location Access Error',
					message: error.message,
				});
				setIsErrorModalOpen(true);
			}
		);
	};

	useEffect(() => {
		if (error) setIsErrorModalOpen(true);
	}, [error]);

	return (
		<div className='w-12 mt-4 p-4 flex flex-col items-center justify-center gap-4 rounded-lg bg-neutral-200/20 backdrop-blur-md'>
			<button type='button' onClick={handleRefreshTLE} className='select-none cursor-pointer p-2 flex items-center justify-center rounded-lg bg-neutral-300/30 hover:bg-neutral-300/50 text-white transition-all duration-300 ease-in-out'>
				<span className='sr-only'>Refresh TLE Data</span>
				<RefreshCcw className='size-4' />
			</button>

			<button type='button' onClick={handleFlyToMyLocation} className='select-none cursor-pointer p-2 flex items-center justify-center rounded-lg bg-neutral-300/30 hover:bg-neutral-300/50 text-white transition-all duration-300 ease-in-out'>
				<span className='sr-only'>My Location</span>
				<MapPin className='size-4' />
			</button>

			<button type='button' onClick={() => setIsLocationsModalOpen(true)} className='select-none cursor-pointer p-2 flex items-center justify-center rounded-lg bg-neutral-300/30 hover:bg-neutral-300/50 text-white transition-all duration-300 ease-in-out'>
				<span className='sr-only'>List Popular Locations</span>
				<Map className='size-4' />
			</button>

			<ErrorModal error={error} open={isErrorModalOpen} onClose={() => setIsErrorModalOpen(false)} />
			<LocationsModal open={isLocationsModalOpen} onClose={() => setIsLocationsModalOpen(false)} />
		</div>
	);
};

export { Toolbar };
