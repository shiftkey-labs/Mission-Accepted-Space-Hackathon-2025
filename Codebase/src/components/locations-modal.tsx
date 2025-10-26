import { X } from 'lucide-react';
import { type FC } from 'react';
import { type LocationType } from '@/types';
import { Dialog, DialogPanel, DialogTitle } from '@headlessui/react';
import { useSatelliteStore } from '@/stores';

const locations: Array<LocationType> = [
	{
		icon: '🇨🇦',
		label: 'Halifax, NS',
		latitude: 44.6488,
		longitude: -63.5752,
	},
	{
		icon: '🇨🇦',
		label: 'Ottawa, ON',
		latitude: 45.4215,
		longitude: -75.6972,
	},
	{
		icon: '🇨🇦',
		label: 'Calgary, AB',
		latitude: 51.0447,
		longitude: -114.0719,
	},
	{
		icon: '🇨🇦',
		label: 'Vancouver, BC',
		latitude: 49.2827,
		longitude: -123.1207,
	},
	{
		icon: '🇨🇦',
		label: 'Yukon Territory',
		latitude: 64.2823,
		longitude: -135.0,
	},
];

interface LocationsModalProps {
	open: boolean;
	onClose: () => void;
}

const LocationsModal: FC<LocationsModalProps> = ({ open, onClose }) => {
	const { flyToLocation } = useSatelliteStore();

	const handleFlyToLocation = (location: LocationType) => {
		if (location.latitude !== null && location.longitude !== null) {
			flyToLocation(location.latitude, location.longitude);
			onClose();
		}
	};

	return (
		<Dialog as='div' open={open} onClose={onClose} className='relative z-10 focus:outline-none'>
			<div className='fixed inset-0 z-10 w-screen overflow-y-auto'>
				<div className='p-4 flex min-h-full items-center justify-center'>
					<DialogPanel transition className='w-full max-w-md p-4 rounded-lg bg-neutral-200/20 backdrop-blur-md transition-all duration-300 ease-in-out data-closed:transform-[scale(95%)] data-closed:opacity-0'>
						<div className='w-full inline-flex items-center justify-between gap-4'>
							<DialogTitle as='h3' className='font-medium font-mono text-xl text-white'>
								Locations
							</DialogTitle>

							<button type='button' onClick={onClose} className='select-none cursor-pointer p-2 flex items-center justify-center rounded-lg bg-neutral-300/30 hover:bg-neutral-300/50 text-white transition-all duration-300 ease-in-out'>
								<span className='sr-only'>Close</span>
								<X className='size-4' />
							</button>
						</div>

						<div className='mt-4 flex flex-col gap-2'>
							{locations.map((location: LocationType, idx: number) => {
								return (
									<button key={idx} type='button' onClick={() => handleFlyToLocation(location)} className='select-none cursor-pointer w-full p-2 flex items-center justify-start gap-2 rounded-lg bg-neutral-300/30 hover:bg-neutral-300/50 text-white transition-all duration-300 ease-in-out'>
										<span className='text-xl'>{location.icon}</span>
										<span className='font-mono text-sm text-white'>{location.label}</span>
									</button>
								);
							})}
						</div>
					</DialogPanel>
				</div>
			</div>
		</Dialog>
	);
};

export { LocationsModal };
