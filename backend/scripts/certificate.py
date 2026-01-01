import argparse
import base64
import datetime
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.x509 import Certificate
from cryptography.x509.oid import NameOID


class CertificateBuilder:
    x509_name: tuple[x509.NameAttribute, ...] = (
        x509.NameAttribute(NameOID.COUNTRY_NAME, "SG"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Singapore"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Singapore"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "NUHS"),
        x509.NameAttribute(NameOID.COMMON_NAME, "medivoice"),
    )

    def __init__(
        self,
        cert_output: Path,
        private_key_output: Path,
        cert_valid_days: int = 365 * 10,
    ) -> None:
        """
        Initialize the CertificateGenerator.

        Args:
            cert_path (Path): The path to save the generated certificate.
            private (Path): The path to save the generated private key.
        """
        self.cert_path = cert_output
        self.private_key_path = private_key_output
        self.cert_valid_days = cert_valid_days

    def build(self) -> None:
        """Generate a self-signed certificate and private key."""
        private_key = self._gen_private_key()

        # Subject and issuer are the same for self-signed certificates
        subject_and_issuer = self._build_subject()

        certificate = self._build_and_sign(private_key, subject_and_issuer)

        self._save_certificate(certificate, self.cert_path)
        self._write_private_key(private_key, self.private_key_path)

        print(f"Certificate saved to {self.cert_path.absolute()}")  # noqa: T201
        print(f"Private key saved to {self.private_key_path.absolute()}")  # noqa: T201
        print(  # noqa: T201
            f"Fingerprint: {base64.urlsafe_b64encode(certificate.fingerprint(hashes.SHA256())).decode()}"
        )

    def _build_subject(self) -> x509.Name:
        """Build the subject for the certificate."""
        return x509.Name(self.x509_name)

    def _build_and_sign(
        self, private_key: RSAPrivateKey, subject_and_issuer: x509.Name
    ) -> Certificate:
        return (
            x509.CertificateBuilder()
            .subject_name(subject_and_issuer)
            .issuer_name(subject_and_issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.now(datetime.UTC))
            .not_valid_after(
                datetime.datetime.now(datetime.UTC)
                + datetime.timedelta(days=self.cert_valid_days)
            )
            .sign(private_key, hashes.SHA256())
        )

    def _gen_private_key(self) -> RSAPrivateKey:
        return rsa.generate_private_key(
            # Using a Fermat number speeds up cryptographic operations
            public_exponent=65537,
            key_size=4096,
        )

    def _write_private_key(self, private_key: RSAPrivateKey, path: Path) -> None:
        path.write_bytes(
            base64.b64encode(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
        )

    def _save_certificate(self, certificate: Certificate, path: Path) -> None:
        path.write_bytes(
            certificate.public_bytes(
                encoding=serialization.Encoding.PEM,
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a self-signed certificate and private key. Note that the private key is encoded to base64 due to AWS Secrets Manager stripping newlines."
    )
    parser.add_argument(
        "certificate", type=str, help="Output file path for the certificate"
    )
    parser.add_argument(
        "private_key", type=str, help="Output file path for the private key"
    )

    args = parser.parse_args()

    certificate_path = Path(args.certificate)
    private_key_path = Path(args.private_key)

    CertificateBuilder(
        cert_output=certificate_path, private_key_output=private_key_path
    ).build()
