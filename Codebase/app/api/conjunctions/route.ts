import { type NextRequest, NextResponse } from "next/server";
import { dataService } from "@/lib/dataService";
import { CANADIAN_SATELLITES } from "@/lib/canadianSatellites";
import type { ConjunctionEvent } from "@/lib/types";

// Risk level priority for sorting
function getRiskPriority(level: string): number {
  switch (level) {
    case "high":
      return 3;
    case "medium":
      return 2;
    case "low":
      return 1;
    default:
      return 0;
  }
}

function generateMockConjunctions(): ConjunctionEvent[] {
  const events: ConjunctionEvent[] = [];
  const now = new Date();

  // Create conjunctions between different Canadian satellites
  const conjunctionScenarios = [
    {
      sat1Idx: 0,
      sat2Idx: 6,
      minRange: 2.5,
      probability: 0.00001,
      hoursFromNow: 12,
      riskLevel: "high" as const,
    },
    {
      sat1Idx: 1,
      sat2Idx: 2,
      minRange: 5.8,
      probability: 0.000001,
      hoursFromNow: 24,
      riskLevel: "medium" as const,
    },
    {
      sat1Idx: 2,
      sat2Idx: 3,
      minRange: 1.2,
      probability: 0.0001,
      hoursFromNow: 6,
      riskLevel: "high" as const,
    },
    {
      sat1Idx: 4,
      sat2Idx: 5,
      minRange: 8.5,
      probability: 0.0000001,
      hoursFromNow: 48,
      riskLevel: "low" as const,
    },
    {
      sat1Idx: 6,
      sat2Idx: 7,
      minRange: 0.8,
      probability: 0.001,
      hoursFromNow: 3,
      riskLevel: "high" as const,
    },
    {
      sat1Idx: 8,
      sat2Idx: 9,
      minRange: 3.2,
      probability: 0.00001,
      hoursFromNow: 18,
      riskLevel: "medium" as const,
    },
    {
      sat1Idx: 10,
      sat2Idx: 11,
      minRange: 6.7,
      probability: 0.000001,
      hoursFromNow: 36,
      riskLevel: "low" as const,
    },
    {
      sat1Idx: 11,
      sat2Idx: 12,
      minRange: 1.5,
      probability: 0.00005,
      hoursFromNow: 9,
      riskLevel: "high" as const,
    },
  ];

  conjunctionScenarios.forEach((scenario, index) => {
    const sat1 = CANADIAN_SATELLITES[scenario.sat1Idx];
    const sat2 = CANADIAN_SATELLITES[scenario.sat2Idx];

    if (!sat1 || !sat2) return;

    const tca = new Date(now.getTime() + scenario.hoursFromNow * 3600 * 1000);

    events.push({
      id: `conj-${index + 1}`,
      satellite1: sat1.name,
      satellite2: sat2.name,
      noradId1: sat1.noradId,
      noradId2: sat2.noradId,
      tca,
      minRange: scenario.minRange,
      probability: scenario.probability,
      relativeVelocity: 10 + Math.random() * 5,
      riskLevel: scenario.riskLevel,
    });
  });

  // Sort by collision risk (probability descending, then min range ascending)
  return events.sort((a, b) => {
    // Primary sort: probability (descending - highest risk first)
    const probDiff = b.probability - a.probability;
    if (probDiff !== 0) return probDiff;

    // Secondary sort: minimum range (ascending - closest first)
    return a.minRange - b.minRange;
  });
}

export async function GET(request: NextRequest) {
  try {
    console.log("[v0 API] Fetching conjunction data...");

    // Use the actual CANADIAN_SATELLITES list directly
    const allConjunctions: any[] = [];

    // Fetch conjunctions for each Canadian satellite using their actual names
    for (const satellite of CANADIAN_SATELLITES) {
      try {
        console.log(
          `[v0 API] Fetching conjunctions for ${satellite.name} (NORAD ${satellite.noradId})`
        );
        const csvData = await dataService.fetchConjunctionsFromCelestrak(
          satellite.name,
          satellite.noradId
        );
        if (csvData) {
          const conjunctions = dataService.parseSOCRATESData(
            csvData,
            satellite.name,
            satellite.noradId
          );
          console.log(
            `[v0 API] Found ${conjunctions.length} conjunctions for ${satellite.name}`
          );
          allConjunctions.push(...conjunctions);
        }
      } catch (error) {
        console.log(
          `[v0 API] Failed to fetch conjunctions for ${satellite.name} (NORAD ${satellite.noradId}):`,
          error
        );
      }
    }

    if (allConjunctions.length > 0) {
      console.log(
        "[v0 API] Returning",
        allConjunctions.length,
        "real conjunction events"
      );

      // Sort by collision risk (probability descending, then min range ascending)
      const sortedConjunctions = allConjunctions.sort((a, b) => {
        // Primary sort: probability (descending - highest risk first)
        const probDiff = b.probability - a.probability;
        if (probDiff !== 0) return probDiff;

        // Secondary sort: minimum range (ascending - closest first)
        return a.minRange - b.minRange;
      });

      // Set cache control headers to prevent any caching
      return NextResponse.json(sortedConjunctions, {
        headers: {
          "Cache-Control":
            "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
          Pragma: "no-cache",
          Expires: "0",
        },
      });
    }

    console.log("[v0 API] No real conjunction data available, using mock data");
    const mockConjunctions = generateMockConjunctions();
    return NextResponse.json(mockConjunctions, {
      headers: {
        "Cache-Control":
          "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        Pragma: "no-cache",
        Expires: "0",
      },
    });
  } catch (error) {
    console.error("[v0 API] Error in conjunctions API:", error);
    console.log("[v0 API] Error occurred, using mock data");
    const mockConjunctions = generateMockConjunctions();
    return NextResponse.json(mockConjunctions, {
      headers: {
        "Cache-Control":
          "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        Pragma: "no-cache",
        Expires: "0",
      },
    });
  }
}
