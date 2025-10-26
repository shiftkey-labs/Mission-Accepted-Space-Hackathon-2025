import React from 'react'

function Header({ language, setLanguage, t }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">🛰️</div>
          <div className="header-text">
            <h1>{t.title}</h1>
            <p className="subtitle">{t.subtitle}</p>
          </div>
        </div>
        <button 
          className="language-toggle"
          onClick={() => setLanguage(language === 'en' ? 'fr' : 'en')}
        >
          {t.languageToggle}
        </button>
      </div>
    </header>
  )
}

export default Header