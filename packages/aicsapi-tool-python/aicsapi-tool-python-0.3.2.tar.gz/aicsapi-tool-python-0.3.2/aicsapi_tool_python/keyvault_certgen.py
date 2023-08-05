from OpenSSL import crypto
from random import randint
from dotenv import load_dotenv
from aicsapi_tool_python import keyvault_utils 
import base64, sys

def generate_v3cert(asus_account, cert_name):
    '''
    Generates RSA private key along with self-signed X509v3 certificate under current directory.
    Saves key & cert pair in PKCS12 (.pfx) format.

    Parameters
    ----------
    asus_account : str
        ASUS account name, used to fill in credentials in certificate
    cert_name : str
        Desired filename of the combined key & cert pair

    Files generated under working directory
    ---------------------------------------
    key-[cert_name].pem
        2048-bit RSA private key in PEM format
    cert-[cert_name].pem
        X509v3 self-signed certificate signed with the generated private key
    [cert_name].pfx
        pcks12 certificate consisting of generated cert & key, can be imported to Azure Key Vault
    '''

    # Generate private key
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)  # generate RSA key-pair

    # Generate self-signed certificate
    cert = crypto.X509()
    cert.get_subject().C = "TW"
    cert.get_subject().ST = "Taiwan"
    cert.get_subject().L = "Taipei"
    cert.get_subject().O = "Asus Inc."
    cert.get_subject().OU = "AICS"
    cert.get_subject().CN = "asus.com"
    cert.get_subject().emailAddress = "{}@asus.com".format( asus_account )

    cert.set_version(2)
    cert.set_serial_number( randint(65537, 1e9+7) )
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)  # 1 year expiry date
    cert.set_issuer( cert.get_subject() )  # self-sign this certificate

    # For X509v3 extension, set CA: True in basicContraints
    cert.add_extensions([
      crypto.X509Extension(b"basicConstraints", True,
                                  b"CA:TRUE"),
      crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash",
                                  subject=cert),
      ])
    cert.add_extensions([
      crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid:always", issuer=cert)
      ])

    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    # Write key & cert to file in PEM
    open("cert-{}.pem".format(cert_name), 'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open("key-{}.pem".format(cert_name), 'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))


    # Convert key & cert to PKCS12
    pkcs = crypto.PKCS12()
    pkcs.set_privatekey(k)
    pkcs.set_certificate(cert)
    with open('{}.pfx'.format( cert_name ), 'wb', buffering=0) as pfx_file:
        pfx_file.write( pkcs.export() )

def upload_v3cert_to_kv(pfx_certfile):
    '''
    Loads Azure Key Vault URL and Certificate name from './.kvvars' as environment vars.
    Then, imports the selected .pfx certificate to the Key Vault.
    (device-code login to Azure will be required)

    Parameters
    ----------
    pfx_certfile : str
        file name of the .pfx certificate you wish to import
    '''

    # Loads key vault information, then requires login
    load_dotenv('.kvvars')
    client = keyvault_utils.keyvault_client_auth()

    # Loads the .pfx binary file and convert it to base64 string
    with open(pfx_certfile, "rb") as f:
        encodedZip = base64.b64encode(f.read())
        b64cert = encodedZip.decode()

    ret = keyvault_utils.keyvault_import_certificate( client, b64cert )

    return ret