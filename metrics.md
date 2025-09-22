## 📊 Diversity & Concentration Metrics Cheat Sheet

This project uses three key metrics to measure **source concentration and diversity** in search results:  

---

### 1️⃣ Herfindahl–Hirschman Index (HHI)
**Formula:** 

```math
HHI = \sum_{i=1}^{N} s_i^2
```
- $s_i$ = proportion of results from domain $i$
- $N$ = total number of domains  


**Range & Interpretation:**  
| HHI Value | Meaning |
|-----------|---------|
| 1 | All results from a single domain (maximum concentration) |
| ~1/N | Results evenly distributed across domains |
| < 0.15 | Unconcentrated / diverse sources |
| 0.15–0.25 | Moderately concentrated |
| > 0.25 | Highly concentrated / biased distribution |

---

### 2️⃣ Gini Coefficient
**Formula (discrete case):**  

$$
G = \frac{\sum_{i=1}^{n} \sum_{j=1}^{n} |x_i - x_j|}{2 n^2 \bar{x}}
$$
- $x_i$ = number of results from domain $i$
- $n$ = total number of domains  
- $bar{x}$ = mean number of results  

**Alternative (cumulative/proportional) formula:**  

$$
G = \frac{n+1 - 2 \frac{\sum_{i=1}^{n} (n+1-i) x_i}{\sum_{i=1}^{n} x_i}}{n}, \quad x_i \text{ sorted ascending}
$$

**Range & Interpretation:**  
| Gini | Meaning |
|------|---------|
| 0 | Perfect equality (all domains equally represented) |
| 0–0.25 | Low inequality / diverse sources |
| 0.25–0.5 | Moderate inequality |
| 0.5–1 | High inequality / few domains dominate |
| 1 | Maximum inequality (all results from one domain) |

---

### 3️⃣ Shannon Entropy
**Formula:**  

$$
H = - \sum_{i=1}^{N} s_i \cdot \log(s_i)
$$  
- $s_i$ = proportion of results from domain $i$  
- $N$ = total number of domains  

**Interpretation:**  
| Entropy Value | Meaning |
|---------------|---------|
| Low | Results concentrated in few domains / limited diversity |
| Moderate | Some diversity, but uneven representation |
| High | Results well-distributed / broad and balanced perspectives |
