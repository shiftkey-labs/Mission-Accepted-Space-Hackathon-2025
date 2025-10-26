import { type NextRequest, NextResponse } from "next/server";
import { dataService } from "@/lib/dataService";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { noradIds } = body;

    if (!Array.isArray(noradIds)) {
      return NextResponse.json(
        { error: "noradIds must be an array" },
        { status: 400 }
      );
    }

    // Try to fetch from Space-Track if credentials are available
    try {
      const satellites = await dataService.fetchBatchTLE(noradIds);
      if (satellites.size > 0) {
        return NextResponse.json(Object.fromEntries(satellites));
      }
    } catch (error) {
      console.log("Space-Track unavailable, no fallback data available");
    }

    // No fallback data available
    return NextResponse.json({});
  } catch (error) {
    console.error("Error in batch TLE API:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
