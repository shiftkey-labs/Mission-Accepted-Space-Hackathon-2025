import axios from "axios";
import type { Satellite, ConjunctionEvent } from "./types";

// Cache for TLE data
const tleCache: Map<number, { data: Satellite; timestamp: number }> = new Map();
const CACHE_DURATION = 1000 * 60 * 60; // 1 hour

export class DataService {
  private static instance: DataService;
  private spaceTrackToken: string | null = null;

  private constructor() {}

  static getInstance(): DataService {
    if (!DataService.instance) {
      DataService.instance = new DataService();
    }
    return DataService.instance;
  }

  /**
   * Fetch TLE data from Space-Track.org
   * Requires SPACE_TRACK_USERNAME and SPACE_TRACK_PASSWORD env vars
   */
  async fetchTLEFromSpaceTrack(noradId: number): Promise<Satellite | null> {
    try {
      // Check cache first
      const cached = tleCache.get(noradId);
      if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
        console.log(`[v0 DataService] Using cached TLE for NORAD ${noradId}`);
        return cached.data;
      }

      // Authenticate if needed
      if (!this.spaceTrackToken) {
        await this.authenticateSpaceTrack();
      }

      console.log(
        `[v0 DataService] Fetching TLE for NORAD ${noradId} from Space-Track.org`
      );

      // Fetch TLE data
      const response = await axios.get(
        `https://www.space-track.org/basicspacedata/query/class/gp/NORAD_CAT_ID/${noradId}/orderby/EPOCH%20desc/limit/1/format/json`,
        {
          headers: {
            Cookie: `spacetrack_csrf_token=${this.spaceTrackToken}`,
          },
          timeout: 10000,
        }
      );

      if (response.data && response.data.length > 0) {
        const data = response.data[0];
        const satellite: Satellite = {
          noradId: Number.parseInt(data.NORAD_CAT_ID),
          name: data.OBJECT_NAME,
          line1: data.TLE_LINE1,
          line2: data.TLE_LINE2,
          status: "active",
        };

        // Cache the result
        tleCache.set(noradId, { data: satellite, timestamp: Date.now() });
        console.log(
          `[v0 DataService] Successfully fetched TLE for ${satellite.name}`
        );
        return satellite;
      }

      return null;
    } catch (error) {
      console.error(
        `[v0 DataService] Error fetching TLE for NORAD ${noradId}:`,
        error
      );
      return null;
    }
  }

  private async authenticateSpaceTrack(): Promise<void> {
    const username = process.env.SPACE_TRACK_USERNAME;
    const password = process.env.SPACE_TRACK_PASSWORD;

    if (!username || !password) {
      console.log(
        "[v0 DataService] Space-Track credentials not configured, skipping authentication"
      );
      throw new Error("Space-Track credentials not configured");
    }

    try {
      console.log("[v0 DataService] Authenticating with Space-Track.org...");

      const response = await axios.post(
        "https://www.space-track.org/ajaxauth/login",
        new URLSearchParams({
          identity: username,
          password: password,
        }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          timeout: 10000,
        }
      );

      // Extract token from cookies
      const cookies = response.headers["set-cookie"];
      if (cookies) {
        const tokenCookie = cookies.find((c: string) =>
          c.includes("spacetrack_csrf_token")
        );
        if (tokenCookie) {
          this.spaceTrackToken = tokenCookie.split("=")[1].split(";")[0];
          console.log(
            "[v0 DataService] Successfully authenticated with Space-Track.org"
          );
        }
      }
    } catch (error) {
      console.error(
        "[v0 DataService] Space-Track authentication failed:",
        error
      );
      throw error;
    }
  }

  /**
   * Fetch conjunction data from Celestrak SOCRATES using satellite name
   * Returns HTML table data that needs to be parsed
   */
  async fetchConjunctionsFromCelestrak(
    satelliteName: string,
    noradId?: number
  ): Promise<string | null> {
    try {
      console.log(
        `[v0 DataService] Fetching conjunctions for ${satelliteName}${
          noradId ? ` (NORAD ${noradId})` : ""
        } from Celestrak SOCRATES`
      );

      // Use the satellite name directly for SOCRATES query
      const response = await axios.get(
        `https://celestrak.org/SOCRATES/table-socrates.php?NAME=${encodeURIComponent(
          satelliteName
        )},&ORDER=MINRANGE&MAX=500`,
        {
          headers: {
            Accept: "text/html",
          },
          timeout: 15000,
        }
      );

      console.log(
        `[v0 DataService] Successfully fetched conjunction data from Celestrak SOCRATES table`
      );
      console.log(
        `[v0 DataService] Response length: ${response.data.length} characters`
      );
      return response.data;
    } catch (error) {
      console.error(
        `[v0 DataService] Error fetching conjunctions for ${satelliteName}:`,
        error
      );
      return null;
    }
  }

  /**
   * Parse SOCRATES HTML table data into conjunction events
   */
  parseSOCRATESData(
    htmlData: string,
    primarySatelliteName: string = "Sapphire",
    primaryNoradId: number = 39089
  ): ConjunctionEvent[] {
    const events: ConjunctionEvent[] = [];

    try {
      console.log(
        `[v0 DataService] Starting to parse HTML data, length: ${htmlData.length}`
      );

      // Find all table rows with data
      const rowPattern = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
      let rowMatch;
      let eventId = 1;
      let currentTCA = "";
      let currentMinRange = 0;
      let currentRelativeVelocity = 0;

      while ((rowMatch = rowPattern.exec(htmlData)) !== null) {
        const rowContent = rowMatch[1];

        // Skip header rows
        if (rowContent.includes("header") || rowContent.includes("th>")) {
          continue;
        }

        // Extract all td elements from this row
        const tdPattern = /<td[^>]*>([\s\S]*?)<\/td>/gi;
        const cells: string[] = [];
        let tdMatch;

        while ((tdMatch = tdPattern.exec(rowContent)) !== null) {
          // Clean up the cell content
          const cellContent = tdMatch[1]
            .replace(/<[^>]*>/g, "")
            .replace(/&nbsp;/g, " ")
            .trim();
          cells.push(cellContent);
        }

        if (cells.length < 6) continue;

        // Check if this row contains TCA data (has rowspan)
        if (
          rowContent.includes("rowspan") &&
          cells[4] &&
          cells[4].match(/\d{4}-\d{2}-\d{2}/)
        ) {
          currentTCA = cells[4];
          currentMinRange = Number.parseFloat(cells[5]) || 0;
          currentRelativeVelocity = Number.parseFloat(cells[6]) || 0;
        }

        // Check if this row has a NORAD ID and probability
        const noradIdMatch = cells[1]?.match(/(\d+)/);
        const probabilityMatch = cells[4]?.match(/([\d.]+[Ee][+-]?\d+)/);

        if (noradIdMatch && probabilityMatch && currentTCA) {
          const noradId = Number.parseInt(noradIdMatch[1]);
          const satelliteName = cells[2]?.trim() || "Unknown";
          const probability = this.parseScientificNotation(probabilityMatch[1]);

          // Only process secondary satellites (not the primary satellite itself)
          if (noradId !== primaryNoradId && probability > 0) {
            const event: ConjunctionEvent = {
              id: `socrates-${primaryNoradId}-${noradId}-${currentTCA.replace(
                /[:\s-]/g,
                ""
              )}-${eventId++}`,
              satellite1: primarySatelliteName,
              satellite2: satelliteName,
              noradId1: primaryNoradId,
              noradId2: noradId,
              tca: new Date(currentTCA),
              minRange: currentMinRange,
              probability,
              relativeVelocity: currentRelativeVelocity,
              riskLevel: this.calculateRiskLevel(currentMinRange, probability),
            };

            events.push(event);
          }
        }
      }

      console.log(`[v0 DataService] Found ${events.length} conjunction events`);
    } catch (error) {
      console.error("Error parsing SOCRATES HTML data:", error);
    }

    console.log(
      `Parsed ${events.length} conjunction events from SOCRATES data`
    );
    return events;
  }

  /**
   * Parse scientific notation strings (e.g., "1.327E-05")
   */
  private parseScientificNotation(str: string): number {
    try {
      return Number.parseFloat(str);
    } catch {
      return 0;
    }
  }

  private calculateRiskLevel(
    minRange: number,
    probability: number
  ): "low" | "medium" | "high" {
    if (probability > 0.0001 || minRange < 1) return "high";
    if (probability > 0.00001 || minRange < 5) return "medium";
    return "low";
  }

  /**
   * Fetch TLE data for multiple satellites in batch
   */
  async fetchBatchTLE(noradIds: number[]): Promise<Map<number, Satellite>> {
    const results = new Map<number, Satellite>();

    console.log(
      `[v0 DataService] Fetching TLE data for ${noradIds.length} satellites in batch`
    );

    // Process in parallel with rate limiting
    const batchSize = 5;
    for (let i = 0; i < noradIds.length; i += batchSize) {
      const batch = noradIds.slice(i, i + batchSize);
      const promises = batch.map((id) => this.fetchTLEFromSpaceTrack(id));
      const batchResults = await Promise.all(promises);

      batchResults.forEach((result, index) => {
        if (result) {
          results.set(batch[index], result);
        }
      });

      // Rate limiting delay
      if (i + batchSize < noradIds.length) {
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
    }

    console.log(
      `[v0 DataService] Successfully fetched ${results.size} TLE records`
    );
    return results;
  }

  /**
   * Clear the TLE cache
   */
  clearCache(): void {
    tleCache.clear();
  }

  async fetchCanadianSubsetFromCelestrak(): Promise<Satellite[]> {
    // Match NORAD IDs from CANADIAN_SATELLITES list
    const targetIds = [
      27843, 32382, 46484, 46485, 46486, 43616, 25951, 27511, 24874, 20780,
      21263, 40895, 39147, 39089,
    ];

    console.log(
      `[v0 DataService] Fetching ${targetIds.length} Canadian satellites individually from CelesTrak...`
    );

    const satellites: Satellite[] = [];
    const now = Date.now();

    // Fetch each satellite individually as batch API doesn't work reliably
    for (const noradId of targetIds) {
      try {
        const url = `https://celestrak.org/NORAD/elements/gp.php?CATNR=${noradId}&FORMAT=tle`;
        console.log(`[v0 DataService] Fetching NORAD ${noradId}...`);

        const { data } = await axios.get(url, {
          timeout: 10000,
          headers: {
            "User-Agent": "Satellite-Conjunction-Analysis/1.0",
          },
        });

        if (data && typeof data === "string" && data.length > 50) {
          // Parse TLE format: 3 lines per satellite (name, line1, line2)
          const lines = data.trim().split("\n");
          if (lines.length >= 3) {
            const name = lines[0].trim();
            const line1 = lines[1].trim();
            const line2 = lines[2].trim();

            const satellite: Satellite = {
              noradId,
              name,
              line1,
              line2,
              status: "active",
            };

            satellites.push(satellite);
            tleCache.set(noradId, { data: satellite, timestamp: now });
            console.log(`[v0 DataService] ✓ Fetched ${name}`);
          }
        } else {
          console.warn(
            `[v0 DataService] ✗ No data returned for NORAD ${noradId}`
          );
        }

        // Small delay to avoid rate limiting
        await new Promise((resolve) => setTimeout(resolve, 200));
      } catch (err) {
        console.error(
          `[v0 DataService] ✗ Error fetching NORAD ${noradId}:`,
          err instanceof Error ? err.message : err
        );
      }
    }

    console.log(
      `[v0 DataService] Successfully fetched ${satellites.length} out of ${targetIds.length} satellites`
    );
    return satellites;
  }
}

export const dataService = DataService.getInstance();
