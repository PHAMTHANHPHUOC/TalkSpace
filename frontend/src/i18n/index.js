import { createI18n } from 'vue-i18n'

const i18n = createI18n({
  legacy: false,
  locale: 'vi',
  fallbackLocale: 'en',
  messages: {} // ban đầu rỗng
})

export async function setLocale(locale) {
  const messages = await fetch(`/locales/${locale}.json`).then(res => res.json())
  i18n.global.setLocaleMessage(locale, messages)
  i18n.global.locale.value = locale
}

export default i18n