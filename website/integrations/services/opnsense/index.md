---
title: OPNsense
---

## What is OPNsense

From https://opnsense.org/

:::note
OPNsense is a free and Open-Source FreeBSD-based firewall and routing software. It is licensed under an Open Source Initiative approved license.
:::

:::note
This is based on authentik 2022.4.1 and OPNsense 22.1.6-amd64 installed using https://docs.opnsense.org/manual/install.html. Instructions may differ between versions.
:::

## Preparation

The following placeholders will be used:

- `LDAP Provider Cert` is the public CA signed certificate used for the LDAP Provider
- `authentik.company` is the FQDN of authentik.
- `opnsense-user` is the name of the authentik Service account we'll create.
- `DC=ldap,DC=goauthentik,DC=io` is the Base DN of the LDAP Provider (default)

### Step 1

Create or import a certificate for use with the LDAP Provider (see [authentik Certificates](https://goauthentik.io/docs/core/certificates) for more information)

### Step 2

In authentik, create a service account (under _Directory/Users_) for OPNsense to use as the LDAP Binder.

In this example, we'll use `opnsense-user` as the Service account's username

:::note
Take note of the password for this user as you'll need to give it to OPNsense in _Step 5_.
:::

### Step 3

In authentik, create an _LDAP Application (under _Applications/Applications_) with these settings:

:::note
Only settings that have been modified from default have been listed.
:::

- Name: LDAP
- Slug: ldap

Leave the _Provider_ at the default, create the new LDAP Provider now by clicking the _Create provider_ button.

   - Select type: LDAP Provider
   - Name: LDAP
   - Search group: opensense-user
   - **Protocol Settings**
     - Name: LDAP
     - Certificate: LDAP Provider Cert
 
 Now select select the newly created provider:
 
   - Provider: LDAP

### Step 4

In authentik, create an outpost (under _Applications/Outposts_) of type `LDAP` that uses the LDAP Application you created in _Step 3_.

:::note
Only settings that have been modified from default have been listed.
:::

- Name: LDAP
- Type: LDAP

### Step 5

Add your authentik LDAP server to OPNsense by going to your OPNsense Web UI and clicking the `+` under _System/Access/Servers_.

Change the following fields

- Descriptive name: authentik
- Hostname or IP address: authentik.company
- Transport: SSL - Encrypted
- Bind credentials
  - User DN: CN=opnsense-user,OU=users,DC=ldap,DC=goauthentik,DC=io
  - Password: whatever-you-set (from Step 2)
  - Base DN: DC=ldap,DC=goauthentik,DC=io
- Authentication containers: OU=users,DC=ldap,DC=goauthentik,DC=io;OU=groups,DC=ldap,DC=goauthentik,DC=io
- Extended Query: &(objectClass=user)

![](./opnsense1.png)
### Step 6

In OPNsense, go to _System/Settings/Administration_ and under _Authentication_ at the bottom of that page, add `authentik` to the Server list

![](./opnsense2.png)

## Notes

:::note
Secure LDAP more by creating a group for your `DN Bind` users and restricting the `Search group` of the LDAP Provider to them.
:::
