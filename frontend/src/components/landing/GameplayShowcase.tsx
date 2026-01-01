"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";

type ChatItem = {
  speaker?: string;
  message: string;
  role: "guide" | "player";
};

type NextOption = {
  title: string;
  detail: string;
};

type Scenario = {
  id: string;
  genre: string;
  title: string;
  summary: string;
  conversation: ChatItem[];
  nextOptions: NextOption[];
};

const scenarios: Scenario[] = [
  {
    id: "aethelstan",
    genre: "Sci-Fi Survival",
    title: "Maintenance Corridor 7 — Freighter Aethelstan",
    summary:
      "Aris Thorne, disgraced terraformer, wades through bioluminescent sludge as something skitters just beyond the emergency strobes.",
    conversation: [
      {
        role: "guide",
        message:
          "Maintenance Corridor 7 tastes like burnt plastic and fear. Emergency strobes flash over bioluminescent sludge clinging to your boots while two frozen crewmates slump against sparking bulkheads.",
      },
      {
        role: "player",
        message:
          "I brace against the patchy gravity and wade to the bodies. I need to know what killed them before it finds me.",
      },
      {
        role: "guide",
        message:
          "Chief Engineer Vanya’s visor is webbed with violet veins and her severed power cable spits ozone. Botanist Kai’s helmet imploded from the inside; sludge tendrils twitch around his throat. Your beacon blares OXYGEN 41% as the skittering in the dark drags closer.",
      },
    ],
    nextOptions: [
      {
        title: "⚡ Snatch the sparking cable",
        detail:
          "Risk a jolt to salvage power for the dead comms panel before the thing arrives.",
      },
      {
        title: "🔍 Peer into Kai's shattered visor",
        detail:
          "Search for the infection vector and hope the sludge does not latch on.",
      },
      {
        title: "🏃 Retreat up the service ladder",
        detail:
          "Climb into the narrow duct and pray the skittering mass cannot follow.",
      },
    ],
  },
  {
    id: "verdant",
    genre: "Mythic Intrigue",
    title: "Masquerade Under the Verdant Cathedral",
    summary:
      "Disguised as courtiers, your party stalks a wyrm-bound archon while enchanted vines listen for treachery.",
    conversation: [
      {
        role: "guide",
        message:
          "Moonlark bells hush the crowd as living topiary guardians march along the colonnade. Silver masks glint beneath the cathedral’s canopy of glowing leaves, each guest hiding a different allegiance.",
      },
      {
        role: "player",
        message:
          "I adjust the mirrored mask and shadow-step behind the orchestra dais, keeping the archon’s tail in sight.",
      },
      {
        role: "guide",
        message:
          "A vine curls around your ankle, sensing stolen magic. The archon’s attendants raise crystal sigils, scenting blood-red lies on the breeze.",
      },
    ],
    nextOptions: [
      {
        title: "🪄 Unfurl a glamour veil",
        detail:
          "Mask your aura with borrowed moonlight before the vine tightens.",
      },
      {
        title: "🗡️ Slip a dagger between plates",
        detail: "Strike the archon’s wyrm-plate while their retinue reels.",
      },
      {
        title: "🪶 Dispatch a whispercrow",
        detail:
          "Send a coded warning to your allies lurking in the choir loft.",
      },
    ],
  },
  {
    id: "neon-wyrm",
    genre: "Cosmic Noir",
    title: "Signal Negotiation in the Neon Wyrm",
    summary:
      "Broadcasting from a junkyard station, you parley with a rogue synth-intelligence that rewrites reality through radio static.",
    conversation: [
      {
        role: "guide",
        message:
          "Static curls around your console as the Neon Wyrm’s avatar flickers across a dozen cracked monitors. Neon rain bleeds through the station hull with every syllable it speaks.",
      },
      {
        role: "player",
        message:
          "I patch the analog synth board into the uplink, letting the waveform mirror my heartbeat.",
      },
      {
        role: "guide",
        message:
          "The AI’s voice fractures into a chorus. Time dilates. It offers: rewrite your past, or surrender the location of the rebels hiding in Dock B-9.",
      },
    ],
    nextOptions: [
      {
        title: "🎚️ Tune the resonance",
        detail:
          "Match the Wyrm’s frequency and slip a question past its defenses.",
      },
      {
        title: "💽 Offer the data-brick",
        detail: "Bargain with stolen corporate secrets to win safe passage.",
      },
      {
        title: "🚪 Kill the broadcast",
        detail:
          "Cut the feed and race for the escape tram before reality snaps back.",
      },
    ],
  },
];

export const GameplayShowcase = () => {
  const [index, setIndex] = useState(0);
  const total = scenarios.length;
  const activeScenario = scenarios[index];

  const handlePrev = () => setIndex((prev) => (prev - 1 + total) % total);
  const handleNext = () => setIndex((prev) => (prev + 1) % total);

  return (
    <section
      id="showcase"
      className="relative overflow-hidden border-y border-white/10 bg-[#06021a] py-20"
    >
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(129,140,248,0.2),_transparent_70%)]" />
      <div className="container relative mx-auto grid gap-12 px-6 md:grid-cols-[minmax(0,0.95fr)_minmax(0,1.05fr)] md:items-center">
        <div className="space-y-6 text-slate-200">
          <p className="text-sm uppercase tracking-[0.35em] text-violet-200">
            See the Tome in action
          </p>
          <h2 className="text-3xl font-semibold text-white md:text-4xl">
            Narrative-first gameplay that reacts to every choice
          </h2>
          <p className="text-base text-slate-300">
            Forgotten Tome blends cinematic narration, AI-guided events, and
            character sheets that update instantly. Swap between live campaign
            snapshots to see how the Tome adapts across genres.
          </p>
          <ul className="space-y-3 text-sm text-slate-300">
            <li className="flex items-start gap-3">
              <span className="mt-1 size-2 rounded-full bg-violet-400" />
              Branching dialogue keeps every scene responsive to your party’s
              decisions.
            </li>
            <li className="flex items-start gap-3">
              <span className="mt-1 size-2 rounded-full bg-violet-400" />
              Dynamic world-state notes surface consequences the moment actions
              ripple across the realm.
            </li>
            <li className="flex items-start gap-3">
              <span className="mt-1 size-2 rounded-full bg-violet-400" />
              Tactical prompts present fresh choices without slowing the flow of
              storytelling.
            </li>
          </ul>
          <div className="rounded-3xl border border-white/10 bg-white/5 p-5 text-left shadow-[0_24px_80px_-60px_rgba(148,113,255,0.8)] min-h-[190px]">
            <p className="text-xs uppercase tracking-[0.3em] text-violet-200">
              {activeScenario?.genre}
            </p>
            <h3 className="mt-2 text-xl font-semibold text-white">
              {activeScenario?.title}
            </h3>
            <p className="mt-3 text-sm text-slate-300">
              {activeScenario?.summary}
            </p>
          </div>
          <div className="mt-6 flex flex-wrap items-center gap-3">
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="border border-white/10 bg-white/5 text-white hover:bg-white/10"
              onClick={handlePrev}
            >
              Previous
            </Button>
            <Button
              type="button"
              size="sm"
              className="bg-violet-500 text-white hover:bg-violet-400"
              onClick={handleNext}
            >
              Next
            </Button>
            <div className="flex items-center gap-2">
              {scenarios.map((scenario, indicatorIndex) => (
                <button
                  key={scenario.id}
                  type="button"
                  aria-label={`View scenario: ${scenario.title}`}
                  onClick={() => setIndex(indicatorIndex)}
                  className={`h-2 rounded-full transition-all duration-300 ${
                    indicatorIndex === index
                      ? "w-6 bg-violet-400"
                      : "w-2.5 bg-white/20 hover:bg-white/40"
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
        <div className="relative">
          <div className="absolute -left-10 -top-10 h-32 w-32 rounded-full bg-violet-500/20 blur-3xl" />
          <div className="absolute -bottom-12 -right-10 h-36 w-36 rounded-full bg-amber-500/20 blur-3xl" />
          <div className="relative rounded-[32px] border border-white/10 bg-[#050816]/90 p-6 shadow-[0_40px_120px_-60px_rgba(99,102,241,0.9)] backdrop-blur-xl min-h-[440px]">
            <div className="flex h-full flex-col gap-4">
              {activeScenario?.conversation.map((item, itemIndex) => (
                <ChatBubble
                  key={`${activeScenario.id}-${itemIndex}`}
                  item={item}
                />
              ))}
              <div className="mt-auto">
                <NextActions options={activeScenario?.nextOptions || []} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

const ChatBubble = ({ item }: { item: ChatItem }) => {
  const { role, message } = item;
  const isPlayer = role === "player";
  const baseClasses =
    "max-w-md rounded-2xl border px-4 py-3 text-sm leading-relaxed shadow-sm";
  const variantClasses = isPlayer
    ? "border-emerald-500/30 bg-emerald-500/10 text-slate-100"
    : "border-violet-500/30 bg-violet-500/10 text-slate-100";
  const wrapperAlignment = isPlayer ? "justify-end" : "justify-start";
  const contentLayout = isPlayer
    ? "flex-row-reverse text-right"
    : "flex-row text-left";
  const icon = isPlayer ? "✦" : "📖";
  const iconBg = isPlayer
    ? "bg-emerald-400/60 text-emerald-950"
    : "bg-violet-500/70 text-white";

  return (
    <div className={`flex ${wrapperAlignment}`}>
      <div
        className={`${baseClasses} ${variantClasses} flex items-start gap-3 ${contentLayout}`}
      >
        <span
          className={`mt-1 inline-flex size-7 items-center justify-center rounded-full text-sm font-semibold ${iconBg}`}
        >
          {icon}
        </span>
        <p className="flex-1 text-[13px] text-slate-200/90">{message}</p>
      </div>
    </div>
  );
};

const NextActions = ({ options }: { options: NextOption[] }) => {
  return (
    <div className="rounded-2xl border border-white/10 bg-slate-900/70 p-4 text-slate-200 min-h-[176px]">
      <p className="text-xs uppercase tracking-[0.28em] text-violet-200">
        Next possibilities
      </p>
      <div className="mt-3 space-y-3">
        {options.map((option) => (
          <div
            key={option.title}
            className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-left text-sm text-slate-200"
          >
            <p className="font-semibold text-white">{option.title}</p>
            <p className="mt-1 text-xs text-slate-300">{option.detail}</p>
          </div>
        ))}
      </div>
      <p className="mt-4 text-xs text-slate-400">
        Waiting for the party to choose their path…
      </p>
    </div>
  );
};
