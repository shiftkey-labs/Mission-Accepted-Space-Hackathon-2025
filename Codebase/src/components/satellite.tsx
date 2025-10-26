import { useRef, useEffect, useState, useMemo, type FC } from 'react';
import { useFrame, type ThreeEvent } from '@react-three/fiber';
import * as THREE from 'three';
import type { SatelliteData } from '@/types';
import { useSatelliteStore } from '@/stores';
import { tleToSatrec, propagateSatrecToGeodetic, estimatePeriodSecondsFromSatrec, kmToUnitScale } from '@/utils';

const SHAPE_IS_BOX = false;
const SAT_POINTS = 256;

interface SatelliteProps {
	data: SatelliteData;
	onClick: (data: SatelliteData) => void;
	isSelected: boolean;
	isPaused?: boolean;
}

type Satrec = ReturnType<typeof tleToSatrec>;

type GeodeticPos = {
	latitudeDeg: number;
	longitudeDeg: number;
	heightKm: number;
	positionEcf: {
		x: number;
		y: number;
		z: number;
	};
} | null;

const Satellite: FC<SatelliteProps> = ({ data, onClick, isSelected, isPaused = false }) => {
	const { getTLEFromCache, fetchTLEData, simSpeed } = useSatelliteStore();

	const satRef = useRef<THREE.Mesh>(null);
	const orbitLineRef = useRef<THREE.Line | null>(null);

	const simTimeRef = useRef<number>(Date.now());
	const lastLogRef = useRef<number>(0);

	const [satrec, setSatrec] = useState<Satrec | null>(null);
	const [orbitGeometry, setOrbitGeometry] = useState<THREE.BufferGeometry | null>(null);

	// Initialize TLE or fetch new one
	useEffect(() => {
		let mounted = true;
		const cached = data.noradId ? getTLEFromCache(data.id) : null;

		const setupFromTLE = (line1: string, line2: string) => {
			try {
				const s = tleToSatrec(line1, line2);
				if (mounted) setSatrec(s);
			} catch (error) {
				console.error('Failed to parse TLE for', data.name, error);
			}
		};

		if (cached?.tle) {
			setupFromTLE(cached.tle.line1, cached.tle.line2);
		} else if (data.noradId) {
			(async () => {
				await fetchTLEData(data.id, data.noradId as string);
				const fresh = getTLEFromCache(data.id);

				if (fresh?.tle) {
					setupFromTLE(fresh.tle.line1, fresh.tle.line2);
				}
			})();
		}

		return () => {
			mounted = false;
		};
	}, [data.id, data.noradId, getTLEFromCache, fetchTLEData, data.name]);

	// Compute orbit geometry (sample one orbital period)
	useEffect(() => {
		if (!satrec) {
			return;
		}

		const periodSeconds = estimatePeriodSecondsFromSatrec(satrec) ?? 5400;
		const now = new Date(simTimeRef.current);
		const points: THREE.Vector3[] = [];

		for (let i = 0; i <= SAT_POINTS; i++) {
			const frac = i / SAT_POINTS;
			const t = new Date(now.getTime() + (frac - 0.5) * periodSeconds * 1000);
			const geo = propagateSatrecToGeodetic(satrec, t) as GeodeticPos;

			if (!geo?.positionEcf) {
				continue;
			}

			const { x, y, z } = geo.positionEcf;
			const scale = kmToUnitScale(1);
			// Map ECF (x, y, z) -> Three.js scene coordinates (x, y, z) where
			// Three.js uses +Y as north/up while ECF uses +Z as north. Convert so
			// surface conversion (latLonToVector3) and ECF positions share the same axes:
			// three.x = ecef.x, three.y = ecef.z, three.z = -ecef.y
			const v = new THREE.Vector3(x * scale, z * scale, -y * scale);

			const rUnit = v.length();

			if (rUnit < 0.9 || rUnit > 8) {
				continue; // skip absurd orbits
			}

			points.push(v);
		}

		if (points.length < 8) {
			setOrbitGeometry(null);
			return;
		}

		const geometry = new THREE.BufferGeometry().setFromPoints(points);
		setOrbitGeometry(geometry);
	}, [satrec]);

	// Animate satellite position
	useFrame((_, delta) => {
		if (!isPaused) simTimeRef.current += delta * 1000 * (simSpeed ?? 1);

		if (satrec && satRef.current) {
			const date = new Date(simTimeRef.current);
			const geo = propagateSatrecToGeodetic(satrec, date) as GeodeticPos;

			if (!geo?.positionEcf) {
				return;
			}

			const { x, y, z } = geo.positionEcf;
			const scale = kmToUnitScale(1);

			// Apply the same ECF->Three mapping for the live satellite position
			satRef.current.position.set(x * scale, z * scale, -y * scale);

			const nowSec = Math.floor(simTimeRef.current / 1000);
			const LOG_INTERVAL = 5;

			if (nowSec - lastLogRef.current >= LOG_INTERVAL) {
				lastLogRef.current = nowSec;
				console.log(`[sat-update] ${data.name} (${data.id}) @ ${date.toISOString()} lat:${geo.latitudeDeg.toFixed(2)} lon:${geo.longitudeDeg.toFixed(2)} alt_km:${geo.heightKm.toFixed(1)}`);
			}
		}
	});

	const handleClick = (e: ThreeEvent<MouseEvent>) => {
		e.stopPropagation();
		onClick(data);
	};

	const material = useMemo(
		() =>
			new THREE.LineBasicMaterial({
				color: data.color,
				transparent: true,
				opacity: isSelected ? 0.6 : 0.2,
			}),
		[data.color, isSelected]
	);

	const orbitLine = useMemo(() => {
		if (!orbitGeometry) {
			return null;
		}

		return new THREE.Line(orbitGeometry, material);
	}, [orbitGeometry, material]);

	return (
		<group>
			{orbitLine && (
				<primitive
					object={orbitLine}
					ref={(r: THREE.Line | null) => {
						orbitLineRef.current = r;
					}}
				/>
			)}

			<mesh ref={satRef} onClick={handleClick}>
				{SHAPE_IS_BOX ? (
					<>
						<boxGeometry args={[0.02, 0.02, 0.02]} />
						<meshStandardMaterial color={data.color} emissive={data.color} emissiveIntensity={isSelected ? 1 : 0.5} />
					</>
				) : (
					<>
						<sphereGeometry args={[0.015, 16, 16]} />
						<meshStandardMaterial color={data.color} emissive={data.color} emissiveIntensity={isSelected ? 1.5 : 0.8} metalness={0.1} roughness={0.4} />
					</>
				)}
			</mesh>
		</group>
	);
};

export { Satellite };
