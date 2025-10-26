export function formatDate(date, language = 'en') {
  if (!date) return '-'
  
  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }
  
  return new Intl.DateTimeFormat(language === 'fr' ? 'fr-CA' : 'en-CA', options).format(new Date(date))
}

export function formatTime(date, language = 'en') {
  if (!date) return '-'
  
  const options = {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }
  
  return new Intl.DateTimeFormat(language === 'fr' ? 'fr-CA' : 'en-CA', options).format(new Date(date))
}

export function calculateYearsInOrbit(launchDate) {
  const now = new Date()
  const launch = new Date(launchDate)
  const years = (now - launch) / (1000 * 60 * 60 * 24 * 365.25)
  return years.toFixed(1)
}

export function formatDuration(minutes) {
  if (minutes < 60) {
    return `${Math.round(minutes)}m`
  }
  const hours = Math.floor(minutes / 60)
  const mins = Math.round(minutes % 60)
  return `${hours}h ${mins}m`
}
