import { Footer } from "@/components/landing/Footer";
import { Header } from "@/components/landing/Header";

export default function TermsPage() {
  return (
    <>
      <Header />
      <div className="min-h-screen">
        <main className="mx-auto max-w-3xl px-4 py-20">
          <div className="space-y-10">
            <div className="text-center space-y-2">
              <h1 className="text-3xl font-bold tracking-tight">
                Terms of Service
              </h1>
              <p className="text-sm text-muted-foreground">
                Last updated: September 2025
              </p>
            </div>

            <div className="space-y-10">
              <section className="space-y-4">
                <h2 className="text-xl font-semibold">1. Agreement to Terms</h2>
                <p>
                  By accessing and using Forgotten Tome ("Service"), you agree
                  to be bound by these Terms of Service and our Privacy Policy.
                  Forgotten Tome is operated by Nichara Labs Pte. Ltd.
                  ("Company", "we", "us").
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  2. Description of Service
                </h2>
                <p>
                  Forgotten Tome is an AI-driven interactive narrative platform
                  where users explore dynamic story domains and influence
                  evolving worlds. Our service includes:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Procedural narrative generation</li>
                  <li>Player action interpretation</li>
                  <li>Persistent world-state simulation</li>
                  <li>Optional third-party account integrations</li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  3. User Accounts and Eligibility
                </h2>
                <p>To use Forgotten Tome, you must:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>
                    Be at least 13 years old (or the minimum digital consent age
                    in your jurisdiction if higher) and legally permitted to use
                    online services. Users under 13 may not access or create an
                    account.
                  </li>
                  <li>
                    Provide accurate and complete registration information
                  </li>
                  <li>Maintain the security of your account credentials</li>
                  <li>
                    Accept responsibility for all activities under your account
                  </li>
                  <li>
                    Not use the Service if you are suspended, banned, or barred
                    by applicable law
                  </li>
                </ul>
                <p className="text-sm text-muted-foreground mt-2">
                  Where required by law we may implement additional age or
                  consent verification measures.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">4. Acceptable Use</h2>
                <p>You agree not to:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Use the service for illegal or unauthorized purposes</li>
                  <li>
                    Upload malicious content or attempt to harm our systems
                  </li>
                  <li>Share your account credentials with others</li>
                  <li>Reverse engineer or attempt to extract our algorithms</li>
                  <li>
                    Use the service to spam or send unsolicited communications
                  </li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  5. Payment and Subscription
                </h2>
                <p>
                  Subscription fees are billed in advance and are non-refundable
                  except as specified in our Refund Policy. We reserve the right
                  to change our pricing with 30 days notice.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">6. Data and Privacy</h2>
                <p>
                  Your privacy is important to us. Please review our Privacy
                  Policy to understand how we collect, use, and protect your
                  data. By using our service, you consent to our data practices
                  as described in our Privacy Policy.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  7. Intellectual Property &amp; Generated Content
                </h2>
                <p>
                  Forgotten Tome (software, code, models, prompts, narrative
                  systems, simulation layers, visual design, brand) is owned by
                  Nichara Labs Pte. Ltd. All rights not expressly granted are
                  reserved. Trademarks, logos, and service marks may not be used
                  without our prior written permission.
                </p>
                <p>
                  You retain ownership of your original inputs (text prompts,
                  uploaded data, custom lore notes, character metadata) and
                  grant us a non-exclusive, worldwide, royalty-free license to
                  host, process, transform, transmit, display, and create
                  intermediate representations from them solely to (a) operate
                  and secure the Service, (b) improve quality, safety, and
                  moderation, and (c) comply with legal obligations.
                </p>
                <p>
                  Narrative text, dialogue, world-state updates, item or faction
                  descriptions and other system-produced or system-enhanced
                  elements ("Generated Content") are and remain the intellectual
                  property of Nichara Labs. We grant you a limited, revocable,
                  non-exclusive, non-transferable, non-sublicensable license to:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Display Generated Content within the Service</li>
                  <li>
                    Share screenshots or excerpts (up to reasonable portions) on
                    social media or streaming platforms for personal,
                    non-commercial fan/community purposes
                  </li>
                  <li>
                    Use excerpts in personal, non-commercial creative projects
                    (blogs, fan fiction) with clear attribution to "Forgotten
                    Tome by Nichara Labs"
                  </li>
                </ul>
                <p>
                  Any broader commercial exploitation (including publishing,
                  merchandising, paid distribution, training other models,
                  dataset aggregation, or selling generated story arcs
                  wholesale) requires a separate written license. You may not:
                  remove attribution, resell raw or bulk outputs, misrepresent
                  Generated Content as exclusively authored by you, use it to
                  train competing models, or circumvent rate/usage controls.
                  This license terminates automatically if you materially breach
                  these Terms.
                </p>
                <p>
                  We may analyze usage in aggregated or anonymized form to
                  refine pacing, safety interceptors, and narrative coherence.
                  We do not incorporate your personal data directly into
                  general-purpose foundation model training.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  8. Service Availability
                </h2>
                <p>
                  We strive for high availability but cannot guarantee
                  uninterrupted service. We may perform maintenance that
                  temporarily affects service availability, with advance notice
                  when possible.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  9. Limitation of Liability
                </h2>
                <p>
                  Forgotten Tome is provided "as is" without warranties. Our
                  liability is limited to the amount you paid for the service in
                  the preceding 12 months. We are not liable for indirect,
                  incidental, or consequential damages.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">10. Termination</h2>
                <p>
                  Either party may terminate this agreement at any time. Upon
                  termination, your access will cease, and we may delete your
                  data as described in our Cancellation Policy.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">11. Changes to Terms</h2>
                <p>
                  We may modify these terms at any time. Material changes will
                  be communicated via email or through our service. Continued
                  use after changes constitutes acceptance.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">12. Governing Law</h2>
                <p>
                  These terms are governed by Singapore law. Any disputes will
                  be resolved in Singapore courts.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  13. Contact Information
                </h2>
                <p>
                  For questions about these terms:
                  <br />
                  <br />
                  <strong>Nichara Labs Pte. Ltd.</strong>
                  <br />
                  Email: support@forgottentome.com
                </p>
              </section>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    </>
  );
}
