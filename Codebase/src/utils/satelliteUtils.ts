import * as satellite from 'satellite.js';
import type { SatRec, EciVec3, PositionAndVelocity } from 'satellite.js';

const EARTH_RADIUS_KM = 6371.0;

const tleToSatrec = (line1: string, line2: string): SatRec => satellite.twoline2satrec(line1, line2);

const isReasonableEcf = (v: EciVec3<number>) => {
	if (!v) {
		return false;
	}

	const r = Math.hypot(v.x, v.y, v.z);

	return r > 0.9 * EARTH_RADIUS_KM && r < 8 * EARTH_RADIUS_KM;
};

const propagateSatrecToGeodetic = (
	satrec: SatRec,
	date: Date
): {
	latitudeDeg: number;
	longitudeDeg: number;
	heightKm: number;
	positionEcf: EciVec3<number>;
} | null => {
	const pv: PositionAndVelocity | false = satellite.propagate(satrec, date);

	if (!pv || !pv.position || pv.position === true) {
		return null;
	}

	const positionEci: EciVec3<number> = pv.position;
	const gmst = satellite.gstime(date);
	const geodetic = satellite.eciToGeodetic(positionEci, gmst);
	const positionEcf = satellite.eciToEcf(positionEci, gmst);

	if (!isReasonableEcf(positionEcf)) {
		return null;
	}

	return {
		latitudeDeg: (geodetic.latitude * 180) / Math.PI,
		longitudeDeg: (geodetic.longitude * 180) / Math.PI,
		heightKm: geodetic.height,
		positionEcf,
	};
};

const estimatePeriodSecondsFromSatrec = (satrec: SatRec): number | null => {
	if (!satrec || !Number.isFinite(satrec.no) || satrec.no <= 0) {
		return null;
	}

	const period = ((2 * Math.PI) / satrec.no) * 60;

	return period < 300 || period > 86400 ? null : period;
};

const kmToUnitScale = (km: number): number => km / EARTH_RADIUS_KM;

export { tleToSatrec, propagateSatrecToGeodetic, estimatePeriodSecondsFromSatrec, kmToUnitScale, isReasonableEcf };
