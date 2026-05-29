import { useState } from "react";
import CTA from "./components/CTA";
import FAQ from "./components/FAQ";
import FeatureCard from "./components/FeatureCard";
import Footer from "./components/Footer";
import Hero from "./components/Hero";
import Navbar from "./components/Navbar";
import Section from "./components/Section";
import EvalMock from "./components/mockups/EvalMock";
import UploadMock from "./components/mockups/UploadMock";
import {
  comparison,
  faq,
  features,
  finalCta,
  howItWorks,
  problem,
  security,
  useCases,
} from "./content/site";

export default function App() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <>
      <Navbar mobileOpen={mobileOpen} onToggle={() => setMobileOpen((o) => !o)} />
      <main>
        <Hero />

        <Section id="why" title={problem.title} subtitle={problem.subtitle}>
          <div className="grid gap-6 md:grid-cols-3">
            {problem.cards.map((card) => (
              <div
                key={card.title}
                className="rounded-2xl border border-marketing-border bg-marketing-surface p-6 shadow-sm"
              >
                <div className="mb-3 h-1 w-12 rounded bg-marketing-gold" />
                <h3 className="font-semibold text-marketing-text">{card.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-marketing-muted">{card.description}</p>
              </div>
            ))}
          </div>
        </Section>

        <Section id="how-it-works" title={howItWorks.title} subtitle={howItWorks.subtitle}>
          <div className="grid items-center gap-12 lg:grid-cols-2">
            <div className="space-y-6">
              {howItWorks.steps.map((step) => (
                <div key={step.step} className="flex gap-4">
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-marketing-accent text-sm font-bold text-white">
                    {step.step}
                  </div>
                  <div>
                    <h3 className="font-semibold text-marketing-text">{step.title}</h3>
                    <p className="mt-1 text-sm text-marketing-muted">{step.description}</p>
                  </div>
                </div>
              ))}
              <p className="rounded-lg border border-marketing-gold/30 bg-marketing-gold/5 px-4 py-3 text-sm font-medium text-marketing-text">
                {howItWorks.reassurance}
              </p>
            </div>
            <UploadMock />
          </div>
        </Section>

        <Section id="features" title={features.title} subtitle={features.subtitle}>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {features.items.map((item) => (
              <FeatureCard key={item.title} title={item.title} description={item.description} />
            ))}
          </div>
        </Section>

        <Section id="use-cases" title={useCases.title} subtitle={useCases.subtitle}>
          <div className="grid gap-6 md:grid-cols-2">
            {useCases.items.map((item) => (
              <div
                key={item.role}
                className="rounded-2xl border border-marketing-border bg-marketing-surface p-6 shadow-sm"
              >
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-marketing-text">{item.role}</h3>
                  {"badge" in item && item.badge && (
                    <span className="rounded-full bg-marketing-accent/10 px-2 py-0.5 text-xs font-medium text-marketing-accent">
                      {item.badge}
                    </span>
                  )}
                </div>
                <p className="mt-2 text-sm leading-relaxed text-marketing-muted">{item.description}</p>
              </div>
            ))}
          </div>
        </Section>

        <Section id="security" title={security.title} subtitle={security.subtitle}>
          <div className="grid items-start gap-12 lg:grid-cols-2">
            <div>
              <ul className="space-y-4">
                {security.items.map((item) => (
                  <li key={item} className="flex gap-3 text-sm text-marketing-muted">
                    <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-marketing-gold" />
                    {item}
                  </li>
                ))}
              </ul>
              <p className="mt-6 text-xs text-marketing-muted">{security.disclaimer}</p>
            </div>
            <EvalMock />
          </div>
        </Section>

        <Section id="comparison" title={comparison.title} subtitle={comparison.subtitle}>
          <div className="overflow-hidden rounded-2xl border border-marketing-border">
            <div className="grid grid-cols-2 bg-marketing-dark text-sm font-semibold text-white">
              <div className="border-r border-slate-700 px-6 py-4">{comparison.genericLabel}</div>
              <div className="px-6 py-4">{comparison.domainMindLabel}</div>
            </div>
            {comparison.rows.map((row, i) => (
              <div
                key={row.generic}
                className={`grid grid-cols-2 text-sm ${i % 2 === 0 ? "bg-marketing-surface" : "bg-marketing-bg"}`}
              >
                <div className="border-r border-marketing-border px-6 py-4 text-marketing-muted">{row.generic}</div>
                <div className="px-6 py-4 font-medium text-marketing-text">{row.domainMind}</div>
              </div>
            ))}
          </div>
        </Section>

        <Section id="faq" title={faq.title}>
          <FAQ items={faq.items} />
        </Section>

        <Section id="contact" dark>
          <CTA title={finalCta.title} description={finalCta.description} button={finalCta.button} />
        </Section>
      </main>
      <Footer />
    </>
  );
}
