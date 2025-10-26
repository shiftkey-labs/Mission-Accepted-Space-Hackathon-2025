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

export type { SatelliteData };
