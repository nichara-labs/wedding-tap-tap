"use client";

import { useQuery } from "@tanstack/react-query";
import { useEffect, useRef, useState } from "react";
import PowerBar from "@/components/PowerBar";
import { settings } from "@/lib/settings";

type TapCounts = {
  bride: number;
  groom: number;
};

const fetchWithTimeout = async (
  url: string,
  signal: AbortSignal | undefined,
  timeoutMs: number,
) => {
  const controller = new AbortController();
  let didTimeout = false;

  const timeoutId = setTimeout(() => {
    didTimeout = true;
    controller.abort();
  }, timeoutMs);

  const onAbort = () => controller.abort();
  signal?.addEventListener("abort", onAbort);

  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) {
      throw new Error(`Request failed with ${response.status}`);
    }
    return (await response.json()) as TapCounts;
  } catch (error) {
    if (didTimeout) {
      throw new Error("Request timed out");
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
    signal?.removeEventListener("abort", onAbort);
  }
};

export default function DashboardPage() {
  const { data, isPending, isError } = useQuery<TapCounts>({
    queryKey: ["status"],
    queryFn: ({ signal }) =>
      fetchWithTimeout(`${settings.api_base_url}/taps`, signal, 3000),
    refetchInterval: 500,
  });
  const [hovered, setHovered] = useState(false);
  const threshold = settings.threshold;
  const maxCount = threshold * 2;
  const groomCount = data?.groom ?? 0;
  const brideCount = data?.bride ?? 0;
  const [showVideo, setShowVideo] = useState(false);
  const previousCounts = useRef<TapCounts>({ bride: 0, groom: 0 });
  const hasPrimedCounts = useRef(false);
  const finalVideoRef = useRef<HTMLVideoElement>(null);
  const groomSoundRef = useRef<HTMLAudioElement>(null);
  const brideSoundRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    if (!showVideo && groomCount >= maxCount && brideCount >= maxCount) {
      setShowVideo(true);
    }
  }, [brideCount, groomCount, maxCount, showVideo]);

  useEffect(() => {
    if (showVideo) {
      finalVideoRef.current?.play().catch(() => {});
    }
  }, [showVideo]);

  useEffect(() => {
    if (!data) return;
    if (!hasPrimedCounts.current) {
      previousCounts.current = { bride: brideCount, groom: groomCount };
      hasPrimedCounts.current = true;
      return;
    }

    const prev = previousCounts.current;
    if (prev.groom < threshold && groomCount >= threshold) {
      groomSoundRef.current?.play().catch(() => {});
    }
    if (prev.bride < threshold && brideCount >= threshold) {
      brideSoundRef.current?.play().catch(() => {});
    }
    previousCounts.current = { bride: brideCount, groom: groomCount };
  }, [brideCount, groomCount, data, threshold]);

  return (
    <main className="relative min-h-screen overflow-hidden text-white bg-black flex items-center justify-center">
      <audio ref={groomSoundRef} src="/level-up1.mp3">
        <track kind="captions" label="tap sound" />
      </audio>

      <audio ref={brideSoundRef} src="/level-up2.mp3">
        <track kind="captions" label="tap" />
      </audio>

      <div className="absolute inset-0 bg-[url('/treasurebox.jpg')] bg-cover bg-center" />
      <div className="absolute inset-0 bg-black/35" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.12),transparent_60%)]" />

      {/* dropdown visual */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2">
        <div className="relative group flex flex-col items-center">
          {/* arrow trigger */}
          <div
            className="
      text-white/80
      text-xl
      cursor-default
      select-none
    "
          >
            ▼
          </div>

          {/* dropdown */}
          <div
            className="
    mt-60
    w-[480px]
    rounded-xl
    bg-black/70
    p-4
    flex flex-col items-center gap-3
    opacity-0 scale-95
    group-hover:opacity-100 group-hover:scale-100
    transition-all duration-200
    pointer-events-none
    "
          >
            {/* qr */}
            <div
              className="
          w-full aspect-square
          bg-[url('/qr-code.png')]
          bg-cover bg-center
          rounded-md
        "
            />

            {/* url */}
            <div className="text-white text-xl tracking-wide">
              game.chanelandnicholas.com
            </div>
          </div>
        </div>
      </div>

      <div className="relative z-10 w-full flex justify-between px-16">
        <PowerBar
          count={brideCount}
          baseColor="pink"
          label="Bride"
          maxCount={maxCount}
        />
        <PowerBar
          count={groomCount}
          baseColor="purple"
          label="Groom"
          maxCount={maxCount}
        />
      </div>

      {isPending && (
        <div className="absolute bottom-6 text-white/80 text-lg">
          Loading taps...
        </div>
      )}

      {isError && (
        <div className="absolute bottom-6 text-rose-200 text-lg">
          Connection error. Retrying...
        </div>
      )}

      {showVideo && (
        <video
          ref={finalVideoRef}
          src="https://microbin.nicholaslyz.com/file/mouse-horse-mole"
          autoPlay
          playsInline
          controls
          className="fixed inset-0 w-full h-full object-cover z-50 bg-black"
        >
          <track kind="captions" label="video" />
        </video>
      )}
    </main>
  );
}
