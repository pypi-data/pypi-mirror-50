hash_usage = {
	'description' : 'hash gived string',
    'usage' : [
	    {
		    '[hi]':'hierarchy (e, o, p, n) (default null) e endorsement, o owner, p platform, n null',
		    '[halg]': '(sha1, sha256, sha384, sha512) (default sha256)',
		    'if': 'input file to be hashed',
		    'ic': 'data string to be hashed'
	    }
    ]
}

startup_usage = {
	'description' : 'Use PUT request to start up TPM device',
	'usage': [
		'No input needed'
	]
}

#tpm action usage
tpm_usage = {
    'tpm_startup' : startup_usage,
    'tpm_hash' : hash_usage
}