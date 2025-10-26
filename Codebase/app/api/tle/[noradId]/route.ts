import { type NextRequest, NextResponse } from "next/server";
import { dataService } from "@/lib/dataService";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ noradId: string }> }
) {
  try {
    const { noradId } = await params;
    const noradIdNum = Number.parseInt(noradId);

    if (isNaN(noradIdNum)) {
      return NextResponse.json({ error: "Invalid NORAD ID" }, { status: 400 });
    }

    // Try to fetch from Space-Track if credentials are available
    try {
      const satellite = await dataService.fetchTLEFromSpaceTrack(noradIdNum);
      if (satellite) {
        return NextResponse.json(satellite);
      }
    } catch (error) {
      console.log("Space-Track unavailable, no fallback data available");
    }

    return NextResponse.json({ error: "Satellite not found" }, { status: 404 });
  } catch (error) {
    console.error("Error in TLE API:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
