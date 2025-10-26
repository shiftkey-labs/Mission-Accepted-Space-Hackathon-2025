import { useRef, type FC } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import { useSatelliteStore } from '@/stores';
import * as THREE from 'three';
import { tleToSatrec, propagateSatrecToGeodetic, kmToUnitScale } from '@/utils';

const CameraController: FC = () => {
	const { camera } = useThree();
	const { targetCameraPosition, resetCamera, followSatellite, selectedSatellite, getTLEFromCache } = useSatelliteStore();

	const isAnimating = useRef(false);
	const startPosition = useRef(new THREE.Vector3());
	const startLookAt = useRef(new THREE.Vector3());
	const progress = useRef(0);

	// Animation duration in seconds when flying to a satellite. Increase to slow down.
	const ANIMATION_DURATION = 2.5; // seconds

	// Follow behavior settings
	const FOLLOW_OFFSET = 0.6; // how much further from Earth's center than the satellite we place the camera
	const FOLLOW_LERP = 0.12; // smoothing factor for camera movement when following

	useFrame((_, delta) => {
		// If follow mode is enabled and a satellite is selected, compute live position and move camera to follow
		if (followSatellite && selectedSatellite?.id && selectedSatellite.noradId) {
			const cached = getTLEFromCache(selectedSatellite.id);

			if (cached?.tle) {
				try {
					const satrec = tleToSatrec(cached.tle.line1, cached.tle.line2);
					const geo = propagateSatrecToGeodetic(satrec, new Date());

					if (geo?.positionEcf) {
						const { x, y, z } = geo.positionEcf;
						const scale = kmToUnitScale(1);
						const satPos = new THREE.Vector3(x * scale, z * scale, -y * scale);

						const rUnit = satPos.length();
						const desiredDistance = Math.max(1.2, rUnit + FOLLOW_OFFSET);
						const desiredPos = satPos.clone().normalize().multiplyScalar(desiredDistance);

						// Smoothly move camera toward desiredPos and look at the satellite
						camera.position.lerp(desiredPos, FOLLOW_LERP);
						camera.lookAt(satPos);

						return; // skip normal target animation while following
					}
				} catch (err) {
					// ignore and fall through to normal behavior
					console.warn('Camera follow error', err);
				}
			}
		}

		if (targetCameraPosition && !isAnimating.current) {
			// Start animation
			isAnimating.current = true;
			startPosition.current.copy(camera.position);
			camera.getWorldDirection(startLookAt.current);
			progress.current = 0;
		}

		if (isAnimating.current && targetCameraPosition) {
			// Animate camera using time-based progress (delta / duration)
			progress.current += delta / ANIMATION_DURATION;

			if (progress.current >= 1) {
				// Animation complete
				camera.position.copy(targetCameraPosition);
				camera.lookAt(0, 0, 0); // Look at Earth center
				isAnimating.current = false;
				resetCamera();
			} else {
				// Smooth interpolation (ease in-out)
				const t = progress.current < 0.5 ? 2 * progress.current * progress.current : 1 - Math.pow(-2 * progress.current + 2, 2) / 2;

				camera.position.lerpVectors(startPosition.current, targetCameraPosition, t);
				camera.lookAt(0, 0, 0);
			}
		}
	});

	return null;
};

export { CameraController };
