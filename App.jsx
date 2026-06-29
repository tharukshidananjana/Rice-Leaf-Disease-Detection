import React from 'react';
import { Github, Linkedin, Mail, Phone, ExternalLink, Award, Code, Database, ChevronRight, Briefcase, Download } from 'lucide-react';
import profileImg from './assets/profile.jpg';

const App = () => {
  const skills = ["Python", "Pandas", "Machine Learning Basic", "Data Visualization", "Statistics", "Numpy"];
  
  const certifications = [
    "Fundamental Tools of Data Wrangling - University of Colorado Boulder",
    "What is Data Science? - IBM",
    "Crash Course on Python - Google",
    "Programming in Python - Meta",
    "Python for Data Science, AI & Development - IBM",
    "Introduction to Deep Learning & Neural Networks - IBM"
  ];

  const projects = [
    {
      title: "🌾Rice-Leaf-Disease-Detection",
      desc:  "An AI-powered agricultural platform built with TensorFlow and CNNs that achieves 86% accuracy in identifying 11 rice leaf diseases, offering farmers automated severity analysis, localized support maps, and actionable treatment insights via a multilingual Streamlit interface",
      tools: ["Python","Streamlit","TensorFlow","Keras","OpenCV","NumPy","Folium"" Streamlit-Folium","gTTS"],
      link:  "https://github.com/tharukshidananjana/Rice-Leaf-Disease-Detection",
      livelink:" https://rice-leaf-disease-detection1.streamlit.app/"
    },
    {
      title: "🍃XAI-Tea-Process-Optimizer",
      desc: "Developed an end-to-end Machine Learning pipeline using XGBoost and SHAP to predict tea quality and visualize feature importance. Features a trilingual Streamlit dashboard to ensure localized accessibility for factory operators.",
      tools: ["Python", "XGBoost","SHAP(XAI)","Streamlit"],
      link: "https://github.com/tharukshidananjana/XAI-Tea-Process-Optimizer",
      livelink:"https://xai-tea-process-optimizer.streamlit.app/"
    },
    {
      title: "University Recommendation System",
      desc: "Developed a ranked recommendation engine using Z-Score algorithms to assist students in selecting the most suitable university courses based on preferences.",
      tools: ["Python", "Pandas", "Streamlit"],
      link: "https://github.com/tharukshidananjana/University-course-Recommendation-System"
    },
    {
      title: "🧠 AI-Powered Multilingual Sentiment Analysis Dashboard!",
      desc: " A real-time sentiment analysis tool designed to bridge the gap in understanding customer emotions across different platforms",
      tools: ["Python", "Pandas", "Streamlit"],
      link: "https://github.com/tharukshidananjana/-Real-time-Mental-Health-Sentiment-Analysis/tree/master",
      livelink:"https://real-time-mental-health-sentiment-analysis.streamlit.app/"
    },
    {
      title: "Telco Churn Analyzer",
      desc: "deployed a Machine Learning application that predicts customer retention for telecommunication companies",
      tools: ["Python", "Pandas", "Streamlit","Numpy"],
      link: " https://github.com/tharukshidananjana/Customer-Churn-Prediction",
      livelink:"https://telco-churn-analyzer.streamlit.app/"
    },

    {
      title: "Ceromo Shop Web Platform",
      desc: "A responsive e-commerce interface focusing on user experience and clean UI/UX principles.",
      tools: ["HTML5", "CSS3", "JavaScript"],
      link: "https://github.com/tharukshidananjana/ceromo_shop_website/tree/main/Project/Project"
    }
    
    
  ];

  const customStyles = `
    html { scroll-behavior: smooth; }
    .main-wrapper { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
    .hover-card { transition: all 0.3s ease; border: 1px solid #334155; }
    .hover-card:hover { transform: translateY(-10px); border-color: #3b82f6 !important; box-shadow: 0 20px 30px rgba(0,0,0,0.3); }
    .hover-btn { transition: all 0.3s ease; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; justify-content: center; }
    .hover-btn:hover { transform: scale(1.05); filter: brightness(1.2); }
    
    .profile-container {
      position: relative;
      width: 180px;
      height: 180px;
      margin: 0 auto;
    }
    .profile-glow {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      border-radius: 50%;
      background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
      padding: 5px;
      box-shadow: 0 0 25px rgba(59, 130, 246, 0.4);
    }
    .profile-img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
      border: 4px solid #0f172a;
      background-color: #1e293b;
      display: block; 
    }

    .grid-container { display: grid; grid-template-columns: 1.5fr 1fr; gap: 40px; }

    @media (max-width: 968px) {
      .grid-container { grid-template-columns: 1fr; }
      .hero-title { font-size: 2.8rem !important; }
    }

    @media (max-width: 480px) {
      .hero-title { font-size: 2.2rem !important; }
      .nav-links { display: none !important; }
    }
  `;

  return (
    <div style={{ backgroundColor: '#0f172a', minHeight: '100vh', fontFamily: "'Inter', sans-serif", color: '#f1f5f9' }}>
      <style>{customStyles}</style>

      {/* Navigation */}
      <nav style={{ borderBottom: '1px solid #1e293b', backgroundColor: 'rgba(15, 23, 42, 0.9)', backdropFilter: 'blur(10px)', position: 'sticky', top: 0, zIndex: 100 }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 2rem' }}>
          <div style={{ fontSize: '1.2rem', fontWeight: '800' }}>
            THARUKSHI <span style={{ color: '#3b82f6' }}>DHANANJANA</span>
          </div>
          <div className="nav-links" style={{ display: 'flex', gap: '2rem' }}>
            <a href="#about" style={{ color: '#94a3b8', textDecoration: 'none' }}>About</a>
            <a href="#projects" style={{ color: '#94a3b8', textDecoration: 'none' }}>Work</a>
            <a href="mailto:tharukshidhananjana@gmail.com" style={{ color: '#3b82f6', textDecoration: 'none', fontWeight: 'bold' }}>Contact</a>
          </div>
        </div>
      </nav>

      {/* Hero Header Section */}
      <header id="about" style={{ padding: '80px 20px', textAlign: 'center', background: 'radial-gradient(circle at center, #1e293b 0%, #0f172a 100%)' }}>
        <div className="profile-container">
          <div className="profile-glow">
            { }
            <img src={profileImg} alt="Tharukshi Dhananjana" className="profile-img" />
          </div>
        </div>

        <h1 className="hero-title" style={{ fontSize: '4rem', fontWeight: '900', margin: '20px 0', color: '#fff' }}>Data Scientist</h1>
        <p style={{ fontSize: '1.1rem', color: '#94a3b8', maxWidth: '700px', margin: '0 auto 40px auto', lineHeight: '1.6' }}>
          Undergraduate student specializing in BICT Honours, passionate about turning data into actionable insights and building intelligent systems.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '15px', flexWrap: 'wrap' }}>
          <a href="#" className="hover-btn" style={{ backgroundColor: '#3b82f6', color: 'white', padding: '12px 25px', borderRadius: '8px', textDecoration: 'none', fontWeight: 'bold' }}>
            <Download size={18} /> Download CV
          </a>
          <a href="https://github.com/tharukshidananjana" target="_blank" rel="noopener noreferrer" className="hover-btn" style={{ border: '1px solid #334155', color: 'white', padding: '12px 25px', borderRadius: '8px', textDecoration: 'none' }}>
            <Github size={18}/> GitHub
          </a>
          <a href="https://linkedin.com/in/tharukshi-dhananjana-06563535b/" target="_blank" rel="noopener noreferrer" className="hover-btn" style={{ border: '1px solid #334155', color: 'white', padding: '12px 25px', borderRadius: '8px', textDecoration: 'none' }}>
            <Linkedin size={18}/> LinkedIn
          </a>
        </div>
      </header>

      <main className="main-wrapper">
        <section id="projects" style={{ marginBottom: '80px' }}>
          <h2 style={{ fontSize: '1.8rem', marginBottom: '30px', display: 'flex', alignItems: 'center', gap: '12px' }}><Briefcase color="#3b82f6" /> Featured Projects</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '25px' }}>
            {projects.map((p, i) => (
              <div key={i} className="hover-card" style={{ backgroundColor: '#1e293b', padding: '30px', borderRadius: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
                  <Database size={28} color="#3b82f6" />
                  <a href={p.link} target="_blank" rel="noopener noreferrer" style={{ color: '#94a3b8' }}><ExternalLink size={18} /></a>
                </div>
                <h3 style={{ fontSize: '1.3rem', marginBottom: '10px' }}>{p.title}</h3>
                <p style={{ color: '#94a3b8', fontSize: '0.95rem', lineHeight: '1.6', marginBottom: '20px' }}>{p.desc}</p>
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  {p.tools.map(t => <span key={t} style={{ fontSize: '0.7rem', color: '#3b82f6', backgroundColor: 'rgba(59, 130, 246, 0.1)', padding: '4px 10px', borderRadius: '4px', fontWeight: 'bold' }}>{t}</span>)}
                </div>
              </div>
            ))}
          </div>
        </section>

        <div className="grid-container">
          <section>
            <h2 style={{ fontSize: '1.6rem', marginBottom: '25px', display: 'flex', alignItems: 'center', gap: '12px' }}><Award color="#3b82f6" /> Certifications</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {certifications.map((c, i) => (
                <div key={i} className="hover-card" style={{ padding: '15px 20px', backgroundColor: '#1e293b', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <ChevronRight size={16} color="#3b82f6" />
                  <span style={{ fontSize: '0.9rem' }}>{c}</span>
                </div>
              ))}
            </div>
          </section>

          <aside style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
            <div style={{ backgroundColor: '#1e293b', padding: '25px', borderRadius: '16px', border: '1px solid #334155' }}>
              <h3 style={{ marginBottom: '18px', display: 'flex', alignItems: 'center', gap: '10px', fontSize: '1.1rem' }}><Code size={20} color="#3b82f6" /> Technical Skills</h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {skills.map(s => <span key={s} className="hover-btn" style={{ backgroundColor: '#0f172a', padding: '6px 14px', borderRadius: '6px', fontSize: '0.8rem', border: '1px solid #334155', cursor: 'default' }}>{s}</span>)}
              </div>
            </div>

            <div className="hover-card" style={{ backgroundColor: '#3b82f6', padding: '30px', borderRadius: '16px', color: 'white' }}>
              <h3 style={{ marginBottom: '10px' }}>Hire Me</h3>
              <p style={{ fontSize: '0.85rem', marginBottom: '20px', opacity: '0.9' }}>Looking for Data Science internship opportunities.</p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <a href="tel:+94714218280" style={{ color: 'white', textDecoration: 'none', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '10px' }}><Phone size={16}/> +94 714 218 280</a>
                <a href="mailto:tharukshidhananjana@gmail.com" style={{ color: 'white', textDecoration: 'none', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '10px' }}><Mail size={16}/> tharukshidhananjana@gmail.com</a>
              </div>
            </div>
          </aside>
        </div>
      </main>

      <footer style={{ padding: '60px 20px', textAlign: 'center', color: '#64748b', fontSize: '0.9rem', borderTop: '1px solid #1e293b', marginTop: '40px' }}>
        <p>© 2025 Tharukshi Dhananjana. Built with React & Vite.</p>
      </footer>
    </div>
  );
};

export default App;