use crate::NONCE_SIZE;
use base64::prelude::*;
use serde::{Deserialize, Serialize};
use std::{fmt, str::FromStr};

#[derive(Debug)]
pub struct ParsePayloadError;

#[derive(Serialize, Deserialize)]
pub struct PayloadV1 {
    pub p: u8,      // Policy
    pub n: String,  // Nonce
    pub ct: String, // Ciphertext
}

impl PayloadV1 {
    pub fn pack(p: u8, n: [u8; NONCE_SIZE], ct: Vec<u8>) -> String {
        let n: String = BASE64_STANDARD.encode(n);
        let ct: String = BASE64_STANDARD.encode(ct);

        Self { p, n, ct }.to_string()
    }
}

impl fmt::Display for PayloadV1 {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "v1${}${}${}", self.p, self.n, self.ct,) // "v1${policy}${nonce}${ciphertext}"
    }
}

impl FromStr for PayloadV1 {
    type Err = ParsePayloadError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // Expected: "v1${policy}${nonce}${ciphertext}"

        // "v1", "{policy}", "{nonce}", "{ciphertext}"
        let parts: Vec<&str> = s.split('$').collect();

        if parts.len() != 4 {
            return Err(ParsePayloadError);
        }

        let income_policy: &str = parts[1];
        let income_nonce: &str = parts[2];
        let income_ciphertext: &str = parts[3];

        // Proper convertions
        let p: u8 = income_policy.parse::<u8>().map_err(|_| ParsePayloadError)?;
        let n: String = income_nonce.into();
        let ct: String = income_ciphertext.into();

        Ok(PayloadV1 { p, n, ct })
    }
}
