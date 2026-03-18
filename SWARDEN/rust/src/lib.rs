mod derive_key;
mod payloads;

use aes_gcm::{
    aead::{Aead, KeyInit},
    Aes256Gcm,
};
use base64::prelude::*;
use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
};
use rand::{rng, seq::IndexedRandom};

use crate::derive_key::_derive_key;
use crate::payloads::{v1::PayloadV1, Payloads};

const NONCE_SIZE: usize = 12;

#[pyfunction]
fn encrypt(
    plaintext: &str,
    master_key: &str,
    system_pepper: &str,
    policy_version_opt: Option<u8>,
) -> PyResult<String> {
    let policy_version: u8;

    match policy_version_opt {
        Some(v) => policy_version = v,
        None => policy_version = *[1, 2, 3, 4].choose(&mut rng()).unwrap(),
    }

    let key: [u8; 32] = _derive_key(master_key, system_pepper, policy_version);

    let mut nonce: [u8; NONCE_SIZE] = [0; NONCE_SIZE];
    getrandom::fill(&mut nonce).map_err(|e: getrandom::Error| {
        PyRuntimeError::new_err(format!("Failed to generate nonce ({e})"))
    })?;

    let aesgcm = Aes256Gcm::new(&key.into());

    let ciphertext: Vec<u8> = aesgcm
        .encrypt(&nonce.into(), plaintext.as_bytes().as_ref())
        .map_err(|e: aes_gcm::Error| {
            PyRuntimeError::new_err(format!("Failed to encrypt data ({e})"))
        })?;

    let payload: String = PayloadV1::pack(policy_version, nonce, ciphertext);

    Ok(payload)
}

#[pyfunction]
fn decrypt(payload: &str, master_key: &str, system_pepper: &str) -> PyResult<String> {
    let parsed: Payloads = payload
        .parse()
        .map_err(|e: String| PyValueError::new_err(e))?;

    match parsed {
        Payloads::V1(data) => _decrypt_v1(data, master_key, system_pepper),
        // ...
    }
}

fn _decrypt_v1(payload: PayloadV1, master_key: &str, system_pepper: &str) -> PyResult<String> {
    let nonce: [u8; NONCE_SIZE] = BASE64_STANDARD
        .decode(payload.n)
        .map_err(|_| PyValueError::new_err("Invalid Base64 in nonce"))?
        .try_into()
        .map_err(|_| PyValueError::new_err("Invalid nonce length"))?;

    let ciphertext: Vec<u8> = BASE64_STANDARD
        .decode(payload.ct)
        .map_err(|_| PyValueError::new_err("Invalid Base64 in ciphertext"))?;

    let key: [u8; 32] = _derive_key(master_key, system_pepper, payload.p);

    let aesgcm = Aes256Gcm::new(&key.into());

    let decrypted_bytes: Vec<u8> = aesgcm
        .decrypt(&nonce.into(), ciphertext.as_ref())
        .map_err(|_| PyValueError::new_err("Decryption failed (wrong key or corrupted data)"))?;

    String::from_utf8(decrypted_bytes).map_err(|e: std::string::FromUtf8Error| {
        PyValueError::new_err(format!("Invalid UTF-8 sequence ({e})"))
    })
}

#[pymodule]
mod rust {
    #[pymodule_export]
    use super::encrypt;

    #[pymodule_export]
    use super::decrypt;
}
