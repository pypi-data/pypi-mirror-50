Simple Roaming Certificate
==========================

This package contains the functions for creating all the certificates, keys
etc.  for Govroam, or eduroam.  The certificates are specifically designed to
work well with eduroam/Govroam and include all the features required to
ensure that as many clients as possible are compatible.

It's based heavily on the python cryptography module.

Usage
=====

<code>from simple_roaming_certificate import gencerts

csrsubject, cacert, cakey_enc, csrkey_enc, servercert, crlcert = gencerts(c,st,l,o,ou,cn,crldp,passphrase,bits)

</code>

The following certificate are available for generation:

RootCA
======
To be installed on the client, as a trusted Root Certificate.
If using the CAT, upload this when creating a profile and set the "Name (CN) of Authentication Server" to idp.westeros.zz.
It can be pushed out to clients via a policy, or downloaded in 'mobileconfig' files or published on a web site

Server Cert 
===========
To be installed on the RADIUS IdP.
Put this, along with the Server Key below, on to your RADIUS server and configure as part of the EAP security. Do not install the above Root CA on the server.

Server Key 
==========
To be installed on the RADIUS IdP, as above.

CRL 
===
Publish at the URL <code>https://&lt;cn&gt;/list.crl</code>. It should be accessible by all clients. Whilst not necessary for clients to authenticate it reduces the risk of some clients rejecting the authentication.

RootCA Key 
==========
To be kept safe, along with the password used, and is required for any future server certificates, or to change the CRL


Notes
=====

You can check the certificates by running:

<code>openssl x509 -noout -text -in &lt;certname&gt;</code>

which will work for rootca.pem and server-cert.pem

<code>openssl rsa -in &lt;keyname&gt; -check</code>

which will work for server-key.pem and root-key.pem

<code>openssl crl -noout -text -in &lt;crlfile&gt;</code>

which will work for list.crl

