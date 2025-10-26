import { useRef, type FC } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import { COLORS } from '@/constants';
import * as THREE from 'three';
import { TextureLoader } from 'three';
import { useSatelliteStore } from '@/stores';

interface EarthProps {
	isPaused: boolean;
}

const Earth: FC<EarthProps> = ({ isPaused }) => {
	// rotate the whole group (so clouds rotate with the earth)
	const groupRef = useRef<THREE.Group>(null);
	const { simSpeed } = useSatelliteStore();

	const [dayTexture, nightTexture, cloudsTexture] = useLoader(TextureLoader, [
		//
		'https://unpkg.com/three-globe@2.31.1/example/img/earth-day.jpg',
		'https://unpkg.com/three-globe@2.31.1/example/img/earth-night.jpg',
		'https://unpkg.com/three-globe@2.31.1/example/img/earth-water.png',
	]);

	// Sidereal rotation rate: 2π radians / 86164 seconds
	const SIDEREAL_ROTATION_RATE = (2 * Math.PI) / 86164;

	useFrame((_, delta) => {
		if (groupRef.current && !isPaused) {
			// delta is seconds since last frame
			groupRef.current.rotation.y += SIDEREAL_ROTATION_RATE * delta * (simSpeed ?? 1);
		}
	});

	return (
		<group ref={groupRef}>
			<mesh>
				<sphereGeometry args={[1, 64, 64]} />
				<meshStandardMaterial map={dayTexture} emissiveMap={nightTexture} emissive={COLORS.white} emissiveIntensity={0.8} roughness={0.9} metalness={0.1} />
			</mesh>

			<mesh>
				<sphereGeometry args={[1.01, 64, 64]} />
				<meshStandardMaterial map={cloudsTexture} transparent opacity={0.4} depthWrite={false} />
			</mesh>
		</group>
	);
};

export { Earth };
	