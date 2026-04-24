---
permalink: /
title: "About me"
excerpt: "Postdoctoral Associate at Baylor College of Medicine"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

Hi, I am Hanfeng Lin — a Postdoctoral Associate at <a href="https://www.bcm.edu/">Baylor College of Medicine</a> in Houston, Texas.

I am a chemical biology researcher with a focus on drug design and screening. My research interests span:

<style>
.research-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0 2rem;
}
.research-card {
  border: 1px solid #e5e7eb;
  border-left: 4px solid #52adc8;
  border-radius: 6px;
  padding: 1.1rem 1.1rem 1rem;
  background: #fafafa;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.research-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}
.research-card__icon {
  font-size: 1.6rem;
  color: #52adc8;
  margin-bottom: 0.55rem;
}
.research-card__title {
  font-size: 1.02rem;
  font-weight: 600;
  margin: 0 0 0.35rem 0;
  color: #2a2a2a;
}
.research-card__desc {
  font-size: 0.9rem;
  color: #555;
  margin: 0;
  line-height: 1.45;
}
</style>

<div class="research-grid">
  <div class="research-card">
    <div class="research-card__icon"><i class="fas fa-link"></i></div>
    <div class="research-card__title">Bifunctional Molecules</div>
    <div class="research-card__desc">PROTACs and Molecular Glues for targeted protein degradation</div>
  </div>
  <div class="research-card">
    <div class="research-card__icon"><i class="fas fa-dna"></i></div>
    <div class="research-card__title">Chemoproteomics</div>
    <div class="research-card__desc">Proteome-wide profiling of covalent inhibitor binding kinetics (COOKIE-Pro)</div>
  </div>
  <div class="research-card">
    <div class="research-card__icon"><i class="fas fa-cube"></i></div>
    <div class="research-card__title">Structure-based Computational Biology</div>
    <div class="research-card__desc"><em>In silico</em> modeling of ternary complexes, MD simulation, and FEP-guided lead optimization</div>
  </div>
</div>

I completed my Ph.D. in Chemical, Physical & Structural Biology at Baylor College of Medicine (Houston, US), where I was mentored by <a href="https://www.bcm.edu/people-search/jin-wang-32671">Prof. Jin Wang</a>. Prior to that, I received a First Class Honours BSc in Biochemistry and Pharmacology from the University of Strathclyde (Glasgow, UK) and a B.S. in Pharmacy from China Pharmaceutical University (Nanjing, China).

I enjoy communicating scientific concepts across disciplines, exchanging expertise, and thinking through problems from a reductionist perspective.

To learn more, visit my <a href="https://hanfeng-lin.github.io/cv/">CV page</a>.

<script>
    window.onload = function () {
        setTimeout(function () {
            var archive = document.querySelector("#main>article section");
            if (archive) {
                var children = archive.children;
                var kill = children[children.length - 1];
                archive.removeChild(kill);
            }
        }, 100);
    }
</script>
