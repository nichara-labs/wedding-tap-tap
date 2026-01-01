import { Footer } from "@/components/landing/Footer";
import { Header } from "@/components/landing/Header";

export default function RefundPolicyPage() {
  return (
    <>
      <Header />
      <div className="min-h-screen">
        <main className="mx-auto max-w-3xl px-4 py-20">
          <div className="space-y-10">
            <div className="text-center space-y-2">
              <h1 className="text-3xl font-bold tracking-tight">
                Refund &amp; Dispute Policy
              </h1>
              <p className="text-sm text-muted-foreground">
                Last updated: January 2025
              </p>
            </div>

            <div className="space-y-10">
              <section className="space-y-4">
                <h2 className="text-xl font-semibold">Refund Policy</h2>
                <p>
                  Forgotten Tome does not offer refunds or pro-rated credits.
                  All subscription charges are final once processed, including
                  for partial months of service.
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>
                    Subscriptions renew automatically at the end of each billing
                    cycle unless you cancel before the renewal date.
                  </li>
                  <li>
                    You may cancel at any time through the billing portal. After
                    cancellation, you retain access until the end of the current
                    billing period.
                  </li>
                  <li>
                    No additional fees are charged once a cancellation is in
                    place; future renewals simply stop.
                  </li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">Manage or Cancel</h2>
                <p>
                  Need to make a change to your plan? Manage your subscription
                  in the customer billing portal inside the Forgotten Tome app
                  or reach out to our support team:
                </p>
                <ul className="list-disc pl-6 space-y-2">
                  <li>Email: hello@forgottentome.io</li>
                  <li>
                    Include the account email tied to your subscription so we
                    can help you quickly.
                  </li>
                </ul>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">Dispute Resolution</h2>
                <p>If you have a dispute regarding charges or service:</p>
                <ol className="list-decimal pl-6 space-y-2">
                  <li>
                    Contact our support team first at hello@forgottentome.io
                  </li>
                  <li>
                    We will investigate and respond within 2 business days
                  </li>
                  <li>
                    If unresolved, disputes may be escalated to our management
                    team
                  </li>
                  <li>
                    For payment disputes, you may also contact your payment
                    provider
                  </li>
                </ol>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">Non-Refundable Items</h2>
                <p>
                  All subscription payments, add-ons, and usage charges are
                  non-refundable. Accounts terminated for violating our Terms of
                  Service are not eligible for credits or reinstatement.
                </p>
              </section>

              <section className="space-y-4">
                <h2 className="text-xl font-semibold">Contact Information</h2>
                <p>
                  For refund requests or disputes, contact:
                  <br />
                  <br />
                  <strong>Nichara Labs Pte. Ltd.</strong>
                  <br />
                  Email: hello@forgottentome.io
                  <br />
                  Business Hours: Monday - Friday, 9:00 AM - 6:00 PM (SGT)
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
