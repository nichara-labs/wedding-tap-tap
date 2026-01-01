import {
  BookOpen,
  Compass,
  Crown,
  Earth,
  Flame,
  Map as MapIcon,
  ScrollText,
  Shield,
  Sparkles,
  Swords,
  UsersRound,
  Wand2,
} from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import Book from "public/book.jpg";
import { Footer } from "@/components/landing/Footer";
import { GameplayShowcase } from "@/components/landing/GameplayShowcase";
import { Header } from "@/components/landing/Header";
import { PlanCard } from "@/components/landing/PlanCard";
import { SubscribeForm } from "@/components/landing/SubscribeForm";
import { Button } from "@/components/ui/button";

const heroStats = [
  {
    label: "Living Realms",
    value: "26",
    note: "Each with branching storylines and evolving stakes",
  },
  {
    label: "Dynamic Encounters",
    value: "320+",
    note: "Handcrafted prompts that react to your party",
  },
  {
    label: "Community Quests",
    value: "Weekly",
    note: "Fresh adventures curated by Forgotten Tome keepers",
  },
];

const storyRealms = [
  {
    title: "Echoes of Eldoria",
    description:
      "Navigate luminous ruins where every whispered rune alters the path ahead.",
    difficulty: "Novice Adventurers",
    tags: ["Exploration", "Mystic Ruins", "Co-op Friendly"],
    icon: Compass,
    gradient: "from-indigo-500/20 via-violet-500/10 to-slate-900/40",
  },
  {
    title: "The Ember Court",
    description:
      "Broker fragile alliances between phoenix clans before the solstice flame dies.",
    difficulty: "Skilled Diplomats",
    tags: ["Intrigue", "Time Pressure", "Moral Choices"],
    icon: Flame,
    gradient: "from-amber-500/20 via-rose-400/10 to-slate-900/40",
  },
  {
    title: "Gearsong Citadel",
    description:
      "Lead sky-born rebels through clockwork fortresses fueled by enchanted ether.",
    difficulty: "Veteran Strategists",
    tags: ["Tactics", "Aerial Battles", "Steampunk"],
    icon: Crown,
    gradient: "from-cyan-400/20 via-blue-500/10 to-slate-900/40",
  },
  {
    title: "Myriad Abyss",
    description:
      "Descend into a prismatic void where your memories sculpt the horrors within.",
    difficulty: "Fearless Delvers",
    tags: ["Psychological", "Cosmic", "Solo Challenge"],
    icon: Shield,
    gradient: "from-fuchsia-500/20 via-purple-600/10 to-slate-900/40",
  },
];

const featureHighlights = [
  {
    title: "Branching Destinies",
    description:
      "Every choice meaningfully alters characters, factions, and the world state.",
    icon: Wand2,
  },
  {
    title: "Party-Ready Play",
    description:
      "Invite friends and let the Tome track shared decisions in real time.",
    icon: UsersRound,
  },
  {
    title: "Lore That Remembers",
    description:
      "Persistent journals capture discoveries, relationships, and unfinished quests.",
    icon: ScrollText,
  },
  {
    title: "Cinematic Encounters",
    description:
      "Adaptive scene framing blends narrative prose with tactical prompts.",
    icon: Swords,
  },
  {
    title: "GM Assist Tools",
    description:
      "Build custom branches, import NPC notes, and let the AI co-GM with you.",
    icon: BookOpen,
  },
  {
    title: "Arcane Events",
    description:
      "Weekly world events unlock new relics, factions, and limited quests.",
    icon: Flame,
  },
];

const journeySteps = [
  {
    title: "Choose a Realm",
    description:
      "Select a living story arc or craft your own from our library of seeds.",
    icon: MapIcon,
  },
  {
    title: "Shape the Tale",
    description:
      "Make decisions, roll narrative challenges, and recruit allies to your cause.",
    icon: Swords,
  },
  {
    title: "Chronicle Your Legend",
    description:
      "Save transcripts, generate art, and share highlights with your guild.",
    icon: ScrollText,
  },
];

export default function LandingPage() {
  return (
    <>
      <Header />
      <main className="relative flex min-h-screen flex-col overflow-hidden bg-[#04010d] text-slate-100">
        <section className="relative overflow-hidden pb-24 pt-8">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(129,140,248,0.35),_transparent_68%)]" />
          <div className="absolute inset-0 bg-gradient-to-b from-[#08031b] via-transparent to-[#04010d]" />
          <div className="container relative mx-auto flex flex-col items-center gap-12 px-6">
            <span className="rounded-full border border-violet-500/40 bg-violet-500/10 px-4 py-1 text-xs font-medium uppercase tracking-[0.35em] text-violet-100">
              Story-driven AI Adventure
            </span>
            <Image
              src={Book}
              alt="Book"
              className="h-64 w-64 object-contain drop-shadow-[0_35px_120px_rgba(76,29,149,0.45)]"
              style={{
                maskImage:
                  "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,1) 18%, rgba(0,0,0,1) 82%, rgba(0,0,0,0) 100%), linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(0,0,0,1) 18%, rgba(0,0,0,1) 82%, rgba(0,0,0,0) 100%)",
                WebkitMaskImage:
                  "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,1) 18%, rgba(0,0,0,1) 82%, rgba(0,0,0,0) 100%), linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(0,0,0,1) 18%, rgba(0,0,0,1) 82%, rgba(0,0,0,0) 100%)",
                maskComposite: "intersect",
                WebkitMaskComposite: "source-in",
              }}
              priority
            />
            <div className="max-w-3xl text-center">
              <h1 className="text-4xl font-semibold leading-tight text-white drop-shadow-[0_12px_45px_rgba(148,113,255,0.55)] md:text-6xl">
                Forge your legend in the <br />{" "}
                <span className="leading-relaxed neon-text font-stylish text-5xl md:text-6xl">
                  Forgotten Tome
                </span>
              </h1>
              <p className="mt-6 text-lg text-slate-200 md:text-xl">
                Step into reactive narratives that listen, adapt, and remember.
                Gather companions, uncover ancient secrets, and let the Tome
                weave a saga around every choice you make.
              </p>
              <div className="my-10 w-full max-w-2xl">
                <SubscribeForm />
              </div>
              <div className="mt-8 py-4 flex flex-wrap items-center justify-center gap-4">
                <Button
                  asChild
                  size="lg"
                  className="shadow-[0_24px_70px_-30px_rgba(148,113,255,0.9)]"
                >
                  <Link href="/#showcase" className="flex items-center gap-2">
                    See the Tome
                    <Sparkles />
                  </Link>
                </Button>
                <Button
                  asChild
                  size="lg"
                  variant="secondary"
                  className="border border-white/30 bg-white/10 text-white hover:bg-white/20"
                >
                  <Link href="/#realms">
                    Browse Realms
                    <Earth />
                  </Link>
                </Button>
              </div>
            </div>
            <div className="grid w-full max-w-4xl grid-cols-1 gap-4 md:grid-cols-3">
              {heroStats.map((stat) => (
                <div
                  key={stat.label}
                  className="rounded-2xl border border-white/10 bg-white/5 px-6 py-5 text-center backdrop-blur-xl"
                >
                  <div className="text-3xl font-semibold text-white md:text-4xl">
                    {stat.value}
                  </div>
                  <p className="mt-2 text-xs font-semibold uppercase tracking-[0.3em] text-violet-200">
                    {stat.label}
                  </p>
                  <p className="mt-3 text-sm text-slate-300">{stat.note}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <GameplayShowcase />

        <section
          id="realms"
          className="relative border-y border-white/10 bg-[#05020f] py-20"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(76,29,149,0.25),_transparent_70%)]" />
          <div className="container relative mx-auto px-6">
            <div className="max-w-3xl">
              <p className="text-sm uppercase tracking-[0.35em] text-violet-200">
                Choose your next story
              </p>
              <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">
                Realms that bend with every decision
              </h2>
              <p className="mt-4 text-slate-300">
                Each realm is a living narrative crafted by our lore keepers and
                dynamically guided by Forgotten Tome’s AI storyteller. Solo or
                with friends, carve unforgettable routes through branching
                quests.
              </p>
            </div>
            <div className="mt-12 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
              {storyRealms.map((realm) => {
                const Icon = realm.icon;
                return (
                  <div
                    key={realm.title}
                    className={`group relative flex h-full flex-col overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br ${realm.gradient} p-6 shadow-[0_30px_80px_-50px_rgba(99,102,241,0.9)] backdrop-blur-xl transition-transform duration-300 hover:-translate-y-1`}
                  >
                    <div className="absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
                      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(236,72,153,0.2),_transparent_65%)]" />
                    </div>
                    <div className="relative flex items-start justify-between">
                      <div className="rounded-2xl bg-white/10 p-3 text-violet-100">
                        <Icon className="size-6" />
                      </div>
                      <span className="rounded-full border border-white/20 bg-white/10 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.28em] text-violet-100">
                        {realm.difficulty}
                      </span>
                    </div>
                    <h3 className="relative mt-6 text-2xl font-semibold text-white">
                      {realm.title}
                    </h3>
                    <p className="relative mt-3 text-sm text-slate-200">
                      {realm.description}
                    </p>
                    <div className="relative mt-4 flex flex-wrap gap-2">
                      {realm.tags.map((tag) => (
                        <span
                          key={tag}
                          className="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-xs font-medium text-violet-100"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                    <Button
                      size="sm"
                      variant="secondary"
                      className="relative mt-6 w-full border border-white/30 bg-white/10 text-white hover:bg-white/20"
                    >
                      Enter Realm
                    </Button>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        <section
          id="features"
          className="relative overflow-hidden bg-[#060218] py-20"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(129,140,248,0.18),_transparent_70%)]" />
          <div className="container relative mx-auto px-6">
            <div className="max-w-2xl text-center md:mx-auto">
              <p className="text-sm uppercase tracking-[0.35em] text-violet-200">
                Why adventurers return
              </p>
              <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">
                Tools to keep every session magical
              </h2>
              <p className="mt-4 text-slate-300">
                Forgotten Tome blends cinematic narration with responsive
                mechanics so you can focus on making memorable decisions, not
                managing spreadsheets.
              </p>
            </div>
            <div className="mt-12 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {featureHighlights.map((feature) => {
                const Icon = feature.icon;
                return (
                  <div
                    key={feature.title}
                    className="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-6 shadow-[0_20px_60px_-45px_rgba(148,113,255,0.8)] backdrop-blur-xl transition-transform duration-300 hover:-translate-y-1"
                  >
                    <div className="absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
                      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(79,70,229,0.28),_transparent_60%)]" />
                    </div>
                    <div className="relative flex items-center gap-4">
                      <div className="rounded-2xl bg-violet-500/20 p-3 text-violet-100">
                        <Icon className="size-6" />
                      </div>
                      <h3 className="text-xl font-semibold text-white">
                        {feature.title}
                      </h3>
                    </div>
                    <p className="relative mt-4 text-sm leading-relaxed text-slate-200">
                      {feature.description}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        <section
          id="community"
          className="relative border-t border-white/10 bg-[#050112] py-20"
        >
          <div className="container mx-auto grid max-w-6xl gap-12 px-6 md:grid-cols-[minmax(0,1.2fr)_minmax(0,1fr)]">
            <div>
              <p className="text-sm uppercase tracking-[0.35em] text-violet-200">
                The adventurer journey
              </p>
              <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">
                Chart a course from spark to legend
              </h2>
              <p className="mt-4 text-slate-300">
                Whether you’re a solo storyteller or a guild of friends,
                Forgotten Tome adapts to how you play. Our dynamic narrator
                remembers every triumph and twist, building on your momentum.
              </p>
              <div className="mt-8 space-y-6">
                {journeySteps.map((step) => {
                  const Icon = step.icon;
                  return (
                    <div
                      key={step.title}
                      className="group flex gap-4 rounded-3xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl transition-colors duration-300 hover:border-violet-400/60"
                    >
                      <div className="flex size-12 items-center justify-center rounded-2xl bg-violet-500/20 text-violet-100">
                        <Icon className="size-6" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-white">
                          {step.title}
                        </h3>
                        <p className="mt-1 text-sm text-slate-300">
                          {step.description}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-violet-500/20 via-indigo-500/10 to-slate-900/40 p-8 text-slate-100 shadow-[0_30px_80px_-60px_rgba(148,113,255,0.9)] backdrop-blur-xl">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(236,72,153,0.18),_transparent_65%)]" />
              <div className="relative space-y-6">
                <h3 className="text-2xl font-semibold text-white">
                  Guild Chronicles
                </h3>
                <p className="text-sm text-slate-200">
                  “Our weekly sessions feel like playing inside a living novel.
                  The Tome remembers our choices, callbacks our earlier
                  mistakes, and surprises us with twists we never saw coming.”
                </p>
                <div>
                  <p className="text-base font-semibold text-white">
                    Captain Mira Solis
                  </p>
                  <p className="text-sm text-violet-200">
                    Guildmaster of the Starbound Collective
                  </p>
                </div>
                <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                  <p className="text-xs uppercase tracking-[0.25em] text-violet-200">
                    Guild benefits
                  </p>
                  <ul className="mt-3 space-y-2 text-sm text-slate-200">
                    <li>• Shared story dashboards for every party member</li>
                    <li>• Custom relic and NPC builders with AI flavor text</li>
                    <li>• Weekly community events and seasonal relic drops</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section
          id="pricing"
          className="relative overflow-hidden bg-[#060218] pb-24 pt-20"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(99,102,241,0.22),_transparent_70%)]" />
          <div className="container relative mx-auto px-6">
            <div className="max-w-2xl text-center md:mx-auto">
              <p className="text-sm uppercase tracking-[0.35em] text-violet-200">
                Guild passes
              </p>
              <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">
                Choose how you explore the Tome
              </h2>
              <p className="mt-4 text-slate-300">
                Start free with a guided story or unlock the full guild toolkit
                for collaborative campaigns.
              </p>
            </div>
            <div className="mt-12 grid gap-6 md:grid-cols-2">
              <PlanCard
                title="Wanderer Pass"
                subtitle="Perfect for solo journeys"
                price="Free"
                features={[
                  "Access to 3 rotating realms",
                  "Narrative memory up to 5 chapters",
                  "Community events & leaderboards",
                ]}
              />
              <PlanCard
                title="Guildmaster Pass"
                subtitle="For persistent party sagas"
                price="$12 / mo"
                primary
                features={[
                  "Unlimited realms & custom campaigns",
                  "Shared party dashboards and NPC vault",
                  "Premium relic drops and seasonal arcs",
                ]}
              />
            </div>
          </div>
        </section>

        <section className="relative overflow-hidden bg-gradient-to-b from-[#060218] via-[#04010d] to-[#010007] py-20">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(148,113,255,0.18),_transparent_70%)]" />
          <div className="container relative mx-auto flex flex-col items-center gap-6 px-6 text-center">
            <h2 className="text-3xl font-semibold text-white md:text-4xl">
              The Tome is open. What legend will you write?
            </h2>
            <p className="max-w-2xl text-slate-300">
              Jump into a living story tonight. Forgotten Tome’s AI narrator
              reacts to every choice you make, supporting solo journaling or
              full-party epics.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-4">
              <Button
                asChild
                size="lg"
                variant="secondary"
                className="border border-white/30 bg-white/10 text-white hover:bg-white/20"
              >
                <Link href="mailto:hello@forgottentome.com">
                  Talk with a Lore Keeper
                </Link>
              </Button>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
