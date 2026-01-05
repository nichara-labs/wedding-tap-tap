"use client";

import { useEffect, useRef, useState } from "react";

const THRESHOLD = 10;
const MAX_COUNT = THRESHOLD * 2; // for scaling color intensity

export default function MagicChestGame() {
  const [groomCount, setGroomCount] = useState(0);
  const [brideCount, setBrideCount] = useState(0);
  const [magicCast, setMagicCast] = useState(false);
  const [showVideo, setShowVideo] = useState(false);
  const [audioUnlocked, setAudioUnlocked] = useState(false);

  const bgVideoRef = useRef<HTMLVideoElement>(null);
  const bgmRef = useRef<HTMLAudioElement>(null);
  const magicAudioRef = useRef<HTMLAudioElement>(null);
  const groomSoundRef = useRef<HTMLAudioElement>(null);
  const brideSoundRef = useRef<HTMLAudioElement>(null);

  // ---------- tap handler ----------
  const handleTap = (type: "groom" | "bride") => {
    if (magicCast) return; // block taps after magic

    if (!audioUnlocked) {
      setAudioUnlocked(true);
      bgmRef.current?.play().catch(() => {});
    }

    if (type === "groom") {
      groomSoundRef.current?.play().catch(() => {});
      setGroomCount((c) => Math.min(c + 1, MAX_COUNT));
    } else {
      brideSoundRef.current?.play().catch(() => {});
      setBrideCount((c) => Math.min(c + 1, MAX_COUNT));
    }
  };

  // ---------- magic cast ----------
  useEffect(() => {
    if (
      !magicCast &&
      groomCount >= THRESHOLD &&
      brideCount >= THRESHOLD &&
      groomCount === brideCount
    ) {
      setMagicCast(true);

      // fade out bgm
      if (bgmRef.current) {
        const fadeDuration = 2000; // 2 seconds
        const fadeStep = 50;
        const initialVolume = bgmRef.current.volume;
        let elapsed = 0;

        const fadeInterval = setInterval(() => {
          elapsed += fadeStep;
          const newVolume = Math.max(
            initialVolume * (1 - elapsed / fadeDuration),
            0,
          );
          if (!bgmRef.current) return;
          bgmRef.current.volume = newVolume;

          if (newVolume <= 0) clearInterval(fadeInterval);
        }, fadeStep);
      }

      // play background video
      bgVideoRef.current?.play().catch(() => {});

      // play magic sound
      magicAudioRef.current?.play().catch(() => {});

      // final video after 10s
      setTimeout(() => setShowVideo(true), 10000);
    }
  }, [groomCount, brideCount, magicCast]);

  // ---------- compute power bar color ----------
  const getBarColor = (count: number, baseColor: string) => {
    const ratio = Math.min(count / MAX_COUNT, 1);
    if (baseColor === "purple") {
      const value = Math.floor(200 - 120 * ratio); // 200 -> 80
      return `rgb(${value}, 0, ${value + 55})`; // dark purple
    } else {
      const value = Math.floor(255 - 120 * ratio); // 255 -> 135
      return `rgb(255, ${value}, ${value})`; // dark pink
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-gray-800 flex flex-col items-center justify-end text-white">
      {/* background video */}
      <video
        ref={bgVideoRef}
        src="/background.mp4"
        autoPlay={false}
        muted
        loop
        playsInline
        className="fixed inset-0 w-full h-full object-cover z-0"
      />

      {/* audio */}
      {/* <audio ref={bgmRef} src="/bgm1.mp3" loop /> */}
      <audio ref={magicAudioRef} src="/magic.mp3">
        <track kind="captions" label="Magic sound" />
      </audio>

      <audio ref={groomSoundRef} src="/level-up1.mp3">
        <track kind="captions" label="tap sound" />
      </audio>

      <audio ref={brideSoundRef} src="/level-up2.mp3">
        <track kind="captions" label="tap" />
      </audio>

      {/* center instruction */}
      {/* instruction */}
      {!magicCast && (
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-3xl font-bold text-white z-20">
          Tap, match and open
        </div>
      )}

      {/* power bars */}
      {!magicCast && (
        <>
          <div className="absolute top-8 left-8 w-20 h-[80vh] bg-gray-700 rounded-3xl overflow-hidden shadow-inner flex flex-col justify-end items-center">
            <div
              className="w-full rounded-3xl transition-all duration-200 flex flex-col justify-end items-center text-white font-bold pb-2  text-3xl"
              style={{
                height: `${(groomCount / MAX_COUNT) * 100}%`,
                backgroundColor: getBarColor(groomCount, "purple"),
              }}
            >
              {groomCount}
            </div>
          </div>

          <div className="absolute top-8 right-8 w-20 h-[80vh] bg-gray-700 rounded-3xl overflow-hidden shadow-inner flex flex-col justify-end items-center">
            <div
              className="w-full rounded-3xl transition-all duration-200 flex flex-col justify-end items-center text-white font-bold pb-2  text-3xl"
              style={{
                height: `${(brideCount / MAX_COUNT) * 100}%`,
                backgroundColor: getBarColor(brideCount, "purple"),
              }}
            >
              {brideCount}
            </div>
          </div>
        </>
      )}

      {/* bottom buttons */}
      {!magicCast && (
        <div className="flex gap-6 w-full px-20 pb-20 z-20 relative">
          <button
            type="button" // <-- explicitly added
            onClick={() => handleTap("groom")}
            className="flex-1 py-8 text-2xl font-bold rounded-3xl bg-gradient-to-br from-purple-600 to-fuchsia-600 shadow-2xl active:scale-95 transition z-20"
          >
            Groom
          </button>
          <button
            type="button" // <-- explicitly added
            onClick={() => handleTap("bride")}
            className="flex-1 py-8 text-2xl font-bold rounded-3xl bg-gradient-to-br from-pink-500 to-fuchsia-600 shadow-2xl active:scale-95 transition z-20"
          >
            Bride
          </button>
        </div>
      )}

      {/* final video */}
      {showVideo && (
        <video
          src="/V1 Couple Montage.mp4"
          autoPlay
          playsInline
          controls
          className="fixed inset-0 w-full h-full object-cover z-50 bg-black"
        >
          <track kind="captions" label="video" />
        </video>
      )}
    </div>
  );
}
