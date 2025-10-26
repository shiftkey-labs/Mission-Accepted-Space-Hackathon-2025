import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import * as THREE from 'three';
import { latLonToVector3 } from '@/utils/coordinates';

interface SatelliteData {
	id: number;
	name: string;
	altitude: number;
	inclination: number;
	operator: string;
	launched: string;
	status: string;
	color: string;
	noradId?: string;
}

interface TLEData {
	satelliteId: number;
	tle: { line1: string; line2: string };
	lastUpdated: number;
}

interface SatelliteStore {
	satellites: SatelliteData[];
	selectedSatellite: SatelliteData | null;
	isPaused: boolean;
	tleCache: Record<number, TLEData>;
	isLoadingTLE: boolean;
	targetCameraPosition: THREE.Vector3 | null;
	simSpeed: number;

	setSatellites: (satellites: SatelliteData[]) => void;
	setSelectedSatellite: (satellite: SatelliteData | null) => void;
	togglePause: () => void;
	setIsPaused: (paused: boolean) => void;
	setSimSpeed: (speed: number) => void;

	fetchTLEData: (satelliteId: number, noradId: string) => Promise<void>;
	getTLEFromCache: (satelliteId: number) => TLEData | null;
	clearTLECache: () => void;

	flyToLocation: (lat: number | null, lon: number | null, radius?: number) => void;
	resetCamera: () => void;
	followSatellite: boolean;
	setFollowSatellite: (follow: boolean) => void;
}

const loadSatellitesFromJson = async (): Promise<SatelliteData[]> => {
	try {
		const res = await fetch('/satellites.json');

		if (!res.ok) {
			throw new Error('Failed to load satellites');
		}

		return await res.json();
	} catch (error) {
		console.error('Error loading satellites:', error);
		return [];
	}
};

const useSatelliteStore = create<SatelliteStore>()(
	persist(
		(set, get) => {
			(async () => {
				const satellites = await loadSatellitesFromJson();
				console.log('Loaded satellites:', satellites.length);
				set({
					satellites,
				});
			})();

			return {
				satellites: [],
				selectedSatellite: null,
				isPaused: false,
				simSpeed: 1,
				tleCache: {},
				isLoadingTLE: false,
				targetCameraPosition: null,
				followSatellite: false,

				setSatellites: (sats) => set({ satellites: sats }),
				setSelectedSatellite: (sat) => set({ selectedSatellite: sat }),
				togglePause: () => set((s) => ({ isPaused: !s.isPaused })),
				setIsPaused: (paused) => set({ isPaused: paused }),
				setSimSpeed: (speed) => set({ simSpeed: speed }),
				setFollowSatellite: (follow) => set({ followSatellite: follow }),

				async fetchTLEData(satelliteId, noradId) {
					const { tleCache } = get();

					if (tleCache[satelliteId] && Date.now() - tleCache[satelliteId].lastUpdated < 3600000) {
						return;
					}

					set({
						isLoadingTLE: true,
					});

					try {
						const id = (noradId || '').trim();

						const response = await fetch(`https://celestrak.org/NORAD/elements/gp.php?CATNR=${id}&FORMAT=TLE`);

						if (!response.ok) {
							throw new Error('Failed TLE fetch');
						}

						const text = (await response.text()).trim();
						const l1 = text.split('\n').find((l) => l.startsWith('1 '));
						const l2 = text.split('\n').find((l) => l.startsWith('2 '));

						if (!l1 || !l2) {
							throw new Error('Invalid TLE data');
						}

						set((s) => ({
							tleCache: {
								...s.tleCache,
								[satelliteId]: {
									satelliteId,
									tle: {
										line1: l1.trim(),
										line2: l2.trim(),
									},
									lastUpdated: Date.now(),
								},
							},
							isLoadingTLE: false,
						}));
					} catch (error) {
						console.error('Error fetching TLE data:', error);

						set({
							isLoadingTLE: false,
						});
					}
				},

				getTLEFromCache: (id) => get().tleCache[id] || null,

				clearTLECache: () =>
					set({
						tleCache: {},
					}),

				flyToLocation(lat: number | null, lon: number | null, radius?: number) {
					if (lat == null || lon == null) return;

					const useRadius = typeof radius === 'number' ? radius : 5;

					set({
						targetCameraPosition: latLonToVector3(lat, lon, useRadius, 0.2),
					});
				},

				resetCamera() {
					set({
						targetCameraPosition: null,
					});
				},
			};
		},
		{
			name: 'satellite-storage-v2',
			partialize: (state) => ({
				tleCache: state.tleCache,
			}),
		}
	)
);

export { useSatelliteStore };
