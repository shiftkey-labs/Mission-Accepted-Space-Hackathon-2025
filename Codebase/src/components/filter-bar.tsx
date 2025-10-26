import { useEffect, useState } from 'react';
import { useSatelliteStore } from '@/stores';
import type { SatelliteData } from '@/types';

const LEO_THRESHOLD = 2000; // in km
const MEO_THRESHOLD = 35000; // in km

const getOrbitType = (altitude: number) => {
	if (altitude < LEO_THRESHOLD) {
		return 'LEO';
	}

	if (altitude < MEO_THRESHOLD) {
		return 'MEO';
	}

	if (altitude >= MEO_THRESHOLD) {
		return 'GEO';
	}

	return 'Unknown';
};

interface FilterBarProps {
	onFilterChange: (filtered: SatelliteData[]) => void;
}

const FilterBar = ({ onFilterChange }: FilterBarProps) => {
	const { satellites, setSatellites } = useSatelliteStore();

	const [selectedOperator, setSelectedOperator] = useState<string | null>(null);
	const [selectedOrbit, setSelectedOrbit] = useState<string | null>(null);
	const [selectedStatus, setSelectedStatus] = useState<string | null>(null);
	const [selectedYearRange, setSelectedYearRange] = useState<string | null>(null);
	const [filtered, setFiltered] = useState<SatelliteData[]>(satellites);

	const toggle = (setter: (v: string | null) => void, current: string | null, value: string) => setter(current === value ? null : value);

	const resetFilters = () => {
		setSelectedOperator(null);
		setSelectedOrbit(null);
		setSelectedStatus(null);
		setSelectedYearRange(null);
		setSatellites(satellites);
	};

	useEffect(() => {
		let result = satellites;

		if (selectedOperator) {
			result = result.filter((s) => s.operator.toLowerCase().includes(selectedOperator.toLowerCase()));
		}

		if (selectedOrbit) {
			result = result.filter((s) => getOrbitType(s.altitude) === selectedOrbit);
		}

		if (selectedStatus) {
			result = result.filter((s) => s.status === selectedStatus);
		}

		if (selectedYearRange) {
			const [start, end] = selectedYearRange.split('-').map(Number);

			result = result.filter((s) => {
				const year = Number(s.launched);
				return year >= start && year <= end;
			});
		}

		setFiltered(result);
	}, [satellites, selectedOperator, selectedOrbit, selectedStatus, selectedYearRange]);

	useEffect(() => {
		onFilterChange(filtered);
	}, [filtered, onFilterChange]);

	return (
		<div className='absolute top-0 right-0 z-10 w-full h-8 p-2 flex flex-col sm:flex-row items-center justify-between gap-2 bg-neutral-200/20 backdrop-blur-md'>
			<div className='no-scrollbar px-2 flex flex-nowrap items-center gap-4 overflow-x-auto'>
				<div className='flex items-center gap-1'>
					<span className='text-xs font-mono text-white/80'>Operator:</span>

					{['MDA Space', 'SpaceX', 'Telesat', 'CSA'].map((operator, idx) => (
						<button key={idx} type='button' onClick={() => toggle(setSelectedOperator, selectedOperator, operator)} className={`select-none cursor-pointer px-2 py-1 rounded-md font-mono text-xs whitespace-nowrap transition-all duration-200 ease-in-out ${selectedOperator === operator ? 'bg-white text-black' : 'bg-neutral-300/30 hover:bg-neutral-300/50 text-white'}`}>
							{operator}
						</button>
					))}
				</div>

				<div className='flex items-center gap-1'>
					<span className='text-xs font-mono text-white/80'>Orbit:</span>

					{['LEO', 'MEO', 'GEO'].map((orbit, idx) => (
						<button key={idx} type='button' onClick={() => toggle(setSelectedOrbit, selectedOrbit, orbit)} className={`select-none cursor-pointer px-2 py-1 rounded-md font-mono text-xs whitespace-nowrap transition-all duration-200 ease-in-out ${selectedOrbit === orbit ? 'bg-white text-black' : 'bg-neutral-300/30 hover:bg-neutral-300/50 text-white'}`}>
							{orbit}
						</button>
					))}
				</div>

				<div className='flex items-center gap-1'>
					<span className='text-xs font-mono text-white/80'>Status:</span>

					{['Active', 'Inactive', 'Retired'].map((status, idx) => (
						<button key={idx} type='button' onClick={() => toggle(setSelectedStatus, selectedStatus, status)} className={`select-none cursor-pointer px-2 py-1 rounded-md font-mono text-xs whitespace-nowrap transition-all duration-200 ease-in-out ${selectedStatus === status ? 'bg-white text-black' : 'bg-neutral-300/30 hover:bg-neutral-300/50 text-white'}`}>
							{status}
						</button>
					))}
				</div>

				<div className='flex items-center gap-1'>
					<span className='text-xs font-mono text-white/80'>Year:</span>

					{['2020-2025', '2010-2019', '2000-2009', 'Before 2000'].map((range, idx) => (
						<button key={idx} type='button' onClick={() => toggle(setSelectedYearRange, selectedYearRange, range)} className={`select-none cursor-pointer px-2 py-1 rounded-md font-mono text-xs whitespace-nowrap transition-all duration-200 ease-in-out ${selectedYearRange === range ? 'bg-white text-black' : 'bg-neutral-300/30 hover:bg-neutral-300/50 text-white'}`}>
							{range}
						</button>
					))}
				</div>
			</div>

			<button type='button' onClick={resetFilters} className='select-none cursor-pointer px-2 py-1 rounded-md font-mono text-xs text-white bg-neutral-300/30 hover:bg-neutral-300/50 transition-all duration-200 ease-in-out'>
				Reset
			</button>
		</div>
	);
};

export { FilterBar };
