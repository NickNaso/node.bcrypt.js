{
  "variables": {
    "NODE_VERSION%":"<!(node -p \"process.versions.node.split(\\\".\\\")[0]\")"
  },
  'targets': [
    {
      'target_name': 'bcrypt_lib',
      'sources': [
        'src/blowfish.cc',
        'src/bcrypt.cc',
        'src/bcrypt_node.cc'
      ],
      'defines': [
            '_GNU_SOURCE',
      ],
      'cflags!': [ '-fno-exceptions' ],
      'cflags_cc!': [ '-fno-exceptions' ],
      'dependencies': [
          "<!(node -p \"require('node-addon-api').targets\"):node_addon_api_except",
      ],
      'conditions': [
        ['OS=="win"', {
          "msvs_settings": {
            "VCCLCompilerTool": {
              "ExceptionHandling": 1
            }
          },
          'defines': [
            'uint=unsigned int',
          ]
        }],
        ['OS=="mac"', {
          'cflags+': ['-fvisibility=hidden'],
          "xcode_settings": {
            "CLANG_CXX_LIBRARY": "libc++",
            'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
            'GCC_SYMBOLS_PRIVATE_EXTERN': 'YES', # -fvisibility=hidden
          }
        }],
        ['OS=="zos" and NODE_VERSION <= 16',{
            'cflags': [
              '-qascii',
            ],
            'defines': ["NAPI_DISABLE_CPP_EXCEPTIONS"],
        }],
      ],
    },
  ]
}
