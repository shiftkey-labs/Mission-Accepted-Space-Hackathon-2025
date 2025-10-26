import { useEffect, useMemo, useState } from 'react';
import { type FC } from 'react';
import { Search } from 'lucide-react';
import type { SatelliteData } from '@/types';
import { useSatelliteStore } from '@/stores';
import { tleToSatrec, propagateSatrecToGeodetic, kmToUnitScale } from '@/utils';

interface SatelliteListProps {
	filteredSatellites: SatelliteData[];
}

const SatelliteList: FC<SatelliteListProps> = ({ filteredSatellites }) => {
	const { setSelectedSatellite, fetchTLEData, getTLEFromCache, flyToLocation } = useSatelliteStore();

	const [query, setQuery] = useState<string>('');

	const filtered = useMemo(() => {
		if (!query) {
			return filteredSatellites;
		}

		const q = query.toLowerCase().trim();

		return filteredSatellites.filter((s) => s.name.toLowerCase().includes(q) || (s.operator || '').toLowerCase().includes(q));
	}, [filteredSatellites, query]);

	const handleClick = async (sat: SatelliteData) => {
		setSelectedSatellite(sat);

		// Try to get TLE and compute current lat/lon to fly to
		try {
			if (sat.noradId) {
				await fetchTLEData(sat.id, sat.noradId);

				const cached = getTLEFromCache(sat.id);

				if (cached?.tle) {
					const satrec = tleToSatrec(cached.tle.line1, cached.tle.line2);
					const geo = propagateSatrecToGeodetic(satrec, new Date());

					if (geo) {
						// Compute camera radius: base at Earth's radius (1) + sat altitude scaled, then add a small offset to back off a bit
						const satRadius = 1 + kmToUnitScale(geo.heightKm);
						const cameraRadius = Math.max(1.6, satRadius + 0.6);
						flyToLocation(geo.latitudeDeg, geo.longitudeDeg, cameraRadius);
						return;
					}
				}
			}
		} catch (err) {
			console.warn('Failed to compute position for', sat.name, err);
		}

		// Fallback: if we couldn't compute lat/lon just center on earth
		flyToLocation(null, null);
	};

	useEffect(() => {
		const isSafari = /^((?!chrome|android|crios|fxios).)*safari/i.test(navigator.userAgent);

		if (isSafari) {
			document.body.classList.add('is-safari');
		}
	}, []);

	return (
		<div className='absolute top-4 right-4 z-10 w-72 h-80 max-h-80 flex flex-col overflow-auto rounded-lg bg-neutral-200/20 backdrop-blur-md sat-list'>
			<div className='sticky top-0 z-10 w-full p-4'>
				<div className='relative w-full'>
					<Search className='absolute left-3 top-1/2 -translate-y-1/2 z-10 size-5 text-neutral-300 pointer-events-none' />

					<input type='text' value={query} onChange={(e) => setQuery(e.target.value)} placeholder='Search satellites...' className='w-full pl-10 px-r py-2 rounded-lg bg-[#606060] backdrop-blur-sm text-white transition-all duration-300 ease-in-out placeholder:text-neutral-200 focus:outline-none focus:ring-2 focus:ring-blue-500' />
				</div>
			</div>

			<ul className='px-4 space-y-1'>
				{filtered.map((satellite: SatelliteData, idx: number) => (
					<li key={idx} onClick={() => handleClick(satellite)} className='select-none cursor-pointer px-3 py-2 flex items-center justify-between gap-4 rounded-lg hover:bg-neutral-300/10 transition-all duration-300 ease-in-out'>
						<span className='font-mono text-sm text-white whitespace-nowrap'>{satellite.name}</span>
						<span className='font-mono text-xs text-neutral-300 truncate'>{satellite.operator}</span>
					</li>
				))}

				{filtered.length === 0 && <li className='p-2 font-mono text-xs text-center text-neutral-300'>No results</li>}
			</ul>
		</div>
	);
};

export { SatelliteList };
