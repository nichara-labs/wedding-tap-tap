"use client";

import { useEffect, useRef, useState } from "react";
import Instruction from "../components/Instruction";
import PowerBar from "../components/PowerBar";
import TapButton from "../components/TapButton";

const THRESHOLD = 10;
const MAX_COUNT = THRESHOLD * 2;

export default function MagicChestGamePage() {
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

  const handleTap = (type: "groom" | "bride") => {
    if (magicCast) return;

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
        const fadeDuration = 2000;
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

      bgVideoRef.current?.play().catch(() => {});
      magicAudioRef.current?.play().catch(() => {});

      setTimeout(() => setShowVideo(true), 10000);
    }
  }, [groomCount, brideCount, magicCast]);

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
      <Instruction visible={!magicCast} />

      {/* power bars */}
      {!magicCast && (
        <div className="absolute top-8 left-0 right-0 flex justify-between px-8 z-20">
          <PowerBar count={groomCount} baseColor="purple" label="Groom" />
          <PowerBar count={brideCount} baseColor="purple" label="Bride" />
        </div>
      )}

      {/* bottom buttons */}
      {!magicCast && (
        <div className="flex gap-6 w-full px-20 pb-20 z-20 relative">
          <TapButton type="groom" onTap={handleTap} />
          <TapButton type="bride" onTap={handleTap} />
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
