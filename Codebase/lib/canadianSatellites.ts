import type { Satellite } from "./types";

// Canadian satellites with real NORAD IDs
export const CANADIAN_SATELLITES: Satellite[] = [
  {
    noradId: 27843,
    name: "SCISAT",
    line1: "1 27843U 03036A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 27843  73.9000 180.0000 0004000  90.0000 270.0000 14.77000000000000",
    launchDate: "2003-08-12",
    status: "active",
    operator: "Canadian Space Agency",
    purpose: "Atmospheric Research",
  },
  {
    noradId: 32382,
    name: "RADARSAT-2",
    line1: "1 32382U 07061A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 32382  98.6000 180.0000 0001200  90.0000 270.0000 14.30000000000000",
    launchDate: "2007-12-14",
    status: "active",
    operator: "MDA",
    purpose: "Earth Observation",
  },
  {
    noradId: 46484,
    name: "RADARSAT Constellation Mission 1",
    line1: "1 46484U 19034A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 46484  97.7400 180.0000 0001100  90.0000 270.0000 14.98000000000000",
    launchDate: "2019-06-12",
    status: "active",
    operator: "Canadian Space Agency",
    purpose: "Earth Observation",
  },
  {
    noradId: 46485,
    name: "RADARSAT Constellation Mission 2",
    line1: "1 46485U 19034B   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 46485  97.7400 180.0000 0001100  90.0000 270.0000 14.98000000000000",
    launchDate: "2019-06-12",
    status: "active",
    operator: "Canadian Space Agency",
    purpose: "Earth Observation",
  },
  {
    noradId: 46486,
    name: "RADARSAT Constellation Mission 3",
    line1: "1 46486U 19034C   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 46486  97.7400 180.0000 0001100  90.0000 270.0000 14.98000000000000",
    launchDate: "2019-06-12",
    status: "active",
    operator: "Canadian Space Agency",
    purpose: "Earth Observation",
  },
  {
    noradId: 43616,
    name: "M3MSat",
    line1: "1 43616U 18046A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 43616  97.5000 180.0000 0001500  90.0000 270.0000 15.10000000000000",
    launchDate: "2016-06-22",
    status: "active",
    operator: "Canadian Armed Forces",
    purpose: "Maritime Surveillance",
  },
  {
    noradId: 25951,
    name: "Anik F1",
    line1: "1 25951U 99049A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 25951   0.0600 180.0000 0001000  90.0000 270.0000  1.00270000000000",
    launchDate: "2000-11-21",
    status: "active",
    operator: "Telesat",
    purpose: "Communications",
  },
  {
    noradId: 27511,
    name: "Nimiq 2",
    line1: "1 27511U 02017A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 27511   0.0500 180.0000 0001000  90.0000 270.0000  1.00270000000000",
    launchDate: "2002-12-29",
    status: "active",
    operator: "Telesat",
    purpose: "Communications",
  },
  {
    noradId: 24874,
    name: "MSAT",
    line1: "1 24874U 96032A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 24874   0.0400 180.0000 0001000  90.0000 270.0000  1.00270000000000",
    launchDate: "1996-04-20",
    status: "active",
    operator: "Telesat",
    purpose: "Communications",
  },
  {
    noradId: 20780,
    name: "Anik E1",
    line1: "1 20780U 91050A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 20780   0.0300 180.0000 0001000  90.0000 270.0000  1.00270000000000",
    launchDate: "1991-09-26",
    status: "inactive",
    operator: "Telesat",
    purpose: "Communications",
  },
  {
    noradId: 21263,
    name: "Anik E2",
    line1: "1 21263U 91051A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 21263   0.0300 180.0000 0001000  90.0000 270.0000  1.00270000000000",
    launchDate: "1991-04-04",
    status: "inactive",
    operator: "Telesat",
    purpose: "Communications",
  },
  {
    noradId: 40895,
    name: "CASSIOPE",
    line1: "1 40895U 15052A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 40895  80.9500 180.0000 0015000  90.0000 270.0000 14.85000000000000",
    launchDate: "2013-09-29",
    status: "active",
    operator: "Canadian Space Agency",
    purpose: "Communications & Science",
  },
  {
    noradId: 39147,
    name: "NEOSSat",
    line1: "1 39147U 13005A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 39147  98.5000 180.0000 0001000  90.0000 270.0000 14.30000000000000",
    launchDate: "2013-02-25",
    status: "active",
    operator: "Canadian Space Agency",
    purpose: "Space Surveillance",
  },
  {
    noradId: 39089,
    name: "Sapphire",
    line1: "1 39089U 13009A   24100.50000000  .00000000  00000-0  00000-0 0  9999",
    line2: "2 39089  98.0000 180.0000 0001000  90.0000 270.0000 14.00000000000000",
    launchDate: "2013-02-25",
    status: "active",
    operator: "Canadian Armed Forces",
    purpose: "Space Surveillance",
  },
];

// Generate more realistic TLE data based on current date
export function generateRealisticTLE(satellite: Satellite): Satellite {
  const now = new Date();
  const epochYear = now.getFullYear() % 100;
  const dayOfYear = Math.floor(
    (now.getTime() - new Date(now.getFullYear(), 0, 0).getTime()) / 86400000
  );
  const epochDay =
    dayOfYear +
    (now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds()) / 86400;

  // Update TLE with current epoch
  const line1Parts = satellite.line1.split(" ");
  line1Parts[3] = `${epochYear}${epochDay.toFixed(8).padStart(12, "0")}`;

  return {
    ...satellite,
    line1: line1Parts.join(" "),
  };
}
