import { NextResponse } from "next/server";
import { dataService } from "@/lib/dataService";

export async function GET() {
  try {
    console.log("[v0 API] ==========================================");
    console.log("[v0 API] Satellites API endpoint called");
    console.log(
      "[v0 API] Fetching selected Canadian satellites from CelesTrak..."
    );
    console.log(
      "[v0 API] DataService instance:",
      dataService ? "EXISTS" : "NULL"
    );

    const satellites = await dataService.fetchCanadianSubsetFromCelestrak();

    console.log(
      "[v0 API] Fetch completed, got",
      satellites.length,
      "satellites"
    );
    console.log("[v0 API] ==========================================");

    return NextResponse.json(satellites);
  } catch (error) {
    console.error("[v0 API] ========================================");
    console.error("[v0 API] ERROR in satellites API:", error);
    console.error(
      "[v0 API] Error type:",
      error instanceof Error ? error.constructor.name : typeof error
    );
    console.error(
      "[v0 API] Error message:",
      error instanceof Error ? error.message : String(error)
    );
    console.error(
      "[v0 API] Error stack:",
      error instanceof Error ? error.stack : "N/A"
    );
    console.error("[v0 API] ========================================");
    return NextResponse.json({ error: String(error) }, { status: 500 });
  }
}
