import { Footer } from "@/components/landing/Footer";
import { Header } from "@/components/landing/Header";

export default function PrivacyPage() {
  return (
    <>
      <Header />
      <div className="min-h-screen">
        <main className="mx-auto max-w-3xl px-4 py-20">
          <div className="space-y-10">
            <div className="text-center space-y-2">
              <h1 className="text-3xl font-bold tracking-tight">
                Privacy Policy
              </h1>
              <p className="text-sm text-muted-foreground">
                Last updated: September 2025
              </p>
            </div>

            <div className="space-y-10">
              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  1. Information We Collect
                </h2>
                <p>
                  We collect information you provide directly and automatically
                  when using Forgotten Tome:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>
                    <strong>Account Information:</strong> Name, email address,
                    and payment details
                  </li>
                  <li>
                    <strong>Content Data:</strong> Emails, documents, and files
                    you choose to analyze
                  </li>
                  <li>
                    <strong>Usage Data:</strong> How you interact with our
                    service and features used
                  </li>
                  <li>
                    <strong>Technical Data:</strong> IP address, browser type,
                    and device information
                  </li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  2. How We Use Your Information
                </h2>
                <p>We use your information to:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Provide AI analysis and personalized recommendations</li>
                  <li>Improve our service and develop new features</li>
                  <li>Process payments and manage your account</li>
                  <li>
                    Communicate with you about your account and our service
                  </li>
                  <li>Ensure security and prevent fraud</li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  3. Data Processing and AI
                </h2>
                <p>
                  Forgotten Tome uses artificial intelligence to generate and
                  adapt interactive narrative content:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>
                    Your data is processed by secure AI models to generate
                    insights
                  </li>
                  <li>
                    We do not use your personal data to train our general AI
                    models
                  </li>
                  <li>Processing occurs in secure, encrypted environments</li>
                  <li>
                    You can control what data is analyzed through your settings
                  </li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  4. Data Sharing and Disclosure
                </h2>
                <p>
                  We do not sell your personal data. We may share information
                  only:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>With your explicit consent</li>
                  <li>
                    With service providers who help operate our platform (under
                    strict confidentiality agreements)
                  </li>
                  <li>When required by law or to protect our rights</li>
                  <li>In anonymized, aggregated form for analytics</li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">5. Data Security</h2>
                <p>We implement industry-standard security measures:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>End-to-end encryption for data in transit and at rest</li>
                  <li>Regular security audits and vulnerability assessments</li>
                  <li>Access controls and authentication requirements</li>
                  <li>Secure cloud infrastructure with leading providers</li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">6. Data Retention</h2>
                <p>We retain your data as follows:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>
                    Content data: Until you delete it or cancel your account
                  </li>
                  <li>
                    Account data: For the duration of your account plus 30 days
                  </li>
                  <li>Usage logs: Up to 2 years for security and analytics</li>
                  <li>Payment data: As required by financial regulations</li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  7. Your Rights and Controls
                </h2>
                <p>You have the right to:</p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Access and download your data</li>
                  <li>Correct inaccurate information</li>
                  <li>Delete your data and account</li>
                  <li>Control what data is processed</li>
                  <li>Opt-out of non-essential communications</li>
                  <li>Request data portability</li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  8. Third-Party Integrations
                </h2>
                <p>
                  Forgotten Tome may integrate with third-party services (like
                  Gmail, Google Drive). When you authorize these integrations:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>We only access data you explicitly authorize</li>
                  <li>You can revoke access at any time</li>
                  <li>Third-party privacy policies also apply</li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  9. International Data Transfers
                </h2>
                <p>
                  Your data may be processed in countries other than your own.
                  We ensure appropriate safeguards are in place for
                  international transfers.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  10. Children's & Minor Users' Privacy
                </h2>
                <p>
                  The Service is not available to children under 13. Users 13 or
                  older may access the Service if it is lawful in their
                  jurisdiction; where local law requires guardian consent (e.g.
                  some regions 13–16), the guardian is responsible for
                  oversight. We do not knowingly collect personal information
                  from children under 13; if we discover such data we will
                  delete it. Guardians can contact us to review or request
                  deletion of a minor's data.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  11. Generated Content & Ownership
                </h2>
                <p>
                  System-produced narrative outputs, dialogue, item or faction
                  descriptions, and evolving world-state elements ("Generated
                  Content") are owned by Nichara Labs. Your rights to display
                  and share limited excerpts are governed strictly by the
                  license in our Terms of Service. Broader commercial
                  exploitation requires a separate written agreement. You retain
                  ownership of your original inputs (prompts, uploads, custom
                  notes). Avoid submitting confidential data you do not want
                  processed. We do not use your personal data to train
                  generalized foundation models; we may use aggregated or
                  anonymized signals to enhance safety and quality.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">
                  12. Changes to This Policy
                </h2>
                <p>
                  We may update this privacy policy. Material changes will be
                  communicated via email or through our service at least 30 days
                  before taking effect when legally required. Continued use
                  after the effective date constitutes acceptance.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">13. Contact Us</h2>
                <p>
                  For privacy-related questions or requests:
                  <br />
                  <br />
                  <strong>Nichara Labs Pte. Ltd.</strong>
                  <br />
                  Email: support@forgottentome.com
                  <br />
                  <br />
                  Data Protection Officer: support@forgottentome.com
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
