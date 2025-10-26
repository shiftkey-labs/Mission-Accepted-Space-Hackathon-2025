import * as THREE from 'three';

const latLonToVector3 = (latitude: number, longitude: number, radius: number = 1, altitude: number = 0): THREE.Vector3 => {
	const phi = (90 - latitude) * (Math.PI / 180);
	const theta = (longitude + 180) * (Math.PI / 180);

	const totalRadius = radius + altitude;

	const x = -(totalRadius * Math.sin(phi) * Math.cos(theta));
	const y = totalRadius * Math.cos(phi);
	const z = totalRadius * Math.sin(phi) * Math.sin(theta);

	return new THREE.Vector3(x, y, z);
};

export { latLonToVector3 };
