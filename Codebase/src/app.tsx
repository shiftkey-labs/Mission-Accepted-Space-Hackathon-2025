import { useState } from 'react';
import { useSatelliteStore } from '@/stores';
import { Header, SatelliteStats, SatelliteList, Space, Footer, Copyright } from '@/components';
import { GeminiChat } from '@/components/gemini-chat';
import type { SatelliteData } from '@/types';

const App = () => {
	const { satellites, selectedSatellite } = useSatelliteStore();
	const [
		filteredSatellites,
		// setFilteredSatellites
	] = useState<SatelliteData[]>(satellites);

	return (
		<div className='select-none w-screen h-screen bg-black flex'>
			<GeminiChat />

			<div>
				<Header />

				<SatelliteStats satellite={selectedSatellite} />

				<SatelliteList filteredSatellites={filteredSatellites} />

				<Space
					filteredSatellites={filteredSatellites}
					// setFilteredSatellites={setFilteredSatellites}
				/>

				<Footer filteredSatellites={filteredSatellites} />

				<Copyright />
			</div>
		</div>
	);
};

export { App };

// TODOs / Ideas:
// AR / WebXR Overlay
// Use device camera + “sky overlay” so when the user points their phone to the sky, you show satellites passing overhead.
// Combine with your 3D globe view for spatial awareness.
