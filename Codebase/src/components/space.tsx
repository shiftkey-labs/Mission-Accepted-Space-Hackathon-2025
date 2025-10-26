import { useEffect, type FC } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import type { SatelliteData } from '@/types';
import {
	Earth,
	Satellite,
	//  FilterBar
} from '@/components';
import { useSatelliteStore } from '@/stores';
import { COLORS } from '@/constants';
import { CameraController } from './camera-controller';

const SPACE_SAFE_TAGS = new Set(['input', 'textarea', 'button', 'select']);

interface SpaceProps {
	filteredSatellites: SatelliteData[];
	// setFilteredSatellites: (satellites: SatelliteData[]) => void;
}

const Space: FC<SpaceProps> = ({
	filteredSatellites,
	// setFilteredSatellites
}) => {
	const { satellites, selectedSatellite, setSelectedSatellite, isPaused, setIsPaused } = useSatelliteStore();

	useEffect(() => {
		const shouldLetElementHandleSpace = (el: HTMLElement | null) => {
			if (!el) return false;
			if (el.isContentEditable) return true;

			const tagName = el.tagName.toLowerCase();
			return SPACE_SAFE_TAGS.has(tagName);
		};

		const shouldIgnoreShortcut = (event: KeyboardEvent) => {
			const target = event.target as HTMLElement | null;
			if (shouldLetElementHandleSpace(target)) return true;
			return shouldLetElementHandleSpace(document.activeElement as HTMLElement | null);
		};

		const handleKeyDown = (e: KeyboardEvent) => {
			if (e.code !== 'Space' && e.key !== ' ') return;
			if (shouldIgnoreShortcut(e)) return;

			e.preventDefault();
			setIsPaused(true);
		};

		const handleKeyUp = (e: KeyboardEvent) => {
			if (e.code !== 'Space' && e.key !== ' ') return;
			if (shouldIgnoreShortcut(e)) return;

			e.preventDefault();
			setIsPaused(false);
		};

		window.addEventListener('keydown', handleKeyDown);
		window.addEventListener('keyup', handleKeyUp);

		return () => {
			window.removeEventListener('keydown', handleKeyDown);
			window.removeEventListener('keyup', handleKeyUp);
		};
	}, [setIsPaused]);

	return (
		<>
			{/* <FilterBar onFilterChange={setFilteredSatellites} /> */}

			<Canvas
				camera={{
					position: [3, 2, 3],
					fov: 60,
				}}
				onCreated={({ gl }) => {
					gl.setPixelRatio(window.devicePixelRatio);
					gl.setSize(window.innerWidth, window.innerHeight);
				}}>
				<color attach='background' args={[COLORS.black]} />

				<ambientLight intensity={0.3} />
				<pointLight position={[10, 10, 10]} intensity={1.5} />
				<pointLight position={[-10, -10, -10]} intensity={0.5} color={COLORS.blue} />

				<Stars radius={100} depth={50} count={5000} factor={4} saturation={0} />

				<Earth isPaused={isPaused} />

				<CameraController />

				{(filteredSatellites.length > 0 ? filteredSatellites : satellites).map((satellite, idx) => (
					<Satellite key={idx} data={satellite} onClick={setSelectedSatellite} isSelected={selectedSatellite?.id === satellite.id} isPaused={isPaused} />
				))}

				<OrbitControls enablePan={true} enableZoom={true} enableRotate={true} minDistance={1.5} maxDistance={10} />
			</Canvas>
		</>
	);
};

export { Space };
