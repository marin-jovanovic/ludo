const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({

  chainWebpack: config => {
    config.module
      .rule('img')
      .test(/\.(png|svg|jpg|jpeg|gif|json)$/i)
      .type('asset/resource')
      .end()

  },
})


