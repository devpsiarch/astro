## Planetary Plotter

A simple Python script to calculate and visualize the positions of the planets in our solar system on any given date (it is a helio model only for now, more presets later).

---

### 🛰️ Overview

* Reads essential orbital parameters from `data.txt`.
* Applies error corrections (for the gas giants) using `jiggle.txt`.
* Uses basic astronomical formulas to compute each planet's position in 3D space (in Astronomical Units, AU).
* Generates a series of static plots showing the planetary positions over time.
* Optionally converts these plots into an MP4 animation.

---

### 📁 Repository Structure

```plaintext
astro/                   # Project root
├── data.txt             # Orbital elements for each planet
├── jiggle.txt           # Empirical corrections for gas giants
├── planet.py            # Main script: computes positions and saves plots
├── make_vid.sh          # Helper script: stitches plots into output.mp4
└── plots/               # Output directory for PNG frames (make ur own) 
```

---

### ⚙️ Requirements

* Python 3.x
* Matplotlib
* NumPy

You can install dependencies via:

```bash
pip install numpy matplotlib
```

---

### 🚀 Usage

1. **Adjust parameters**

   * Open `planet.py` and modify:

     * Plotting range (in AU)
     * Time step between frames (e.g., days or fraction thereof)

2. **Run the script**

   ```bash
   python planet.py
   ```

   This will generate a series of PNG files in the `plots/` folder.

3. **Build the video (optional)**

   ```bash
   chmod +x make_vid.sh
   ./make_vid.sh
   ```

   The final animation will be saved as `output.mp4`.

---

### 🎥 Demo

[![Watch the animation](https://raw.githubusercontent.com/devpsiarch/astro/main/assets/fig-0.png)](https://raw.githubusercontent.com/devpsiarch/astro/main/assets/output.mp4)

- in ```Planets.zip``` you will find the plots (100 .png's) that where used to create the same video, unzip them and inspect it dont worry its safe... :)

---

### ✏️ Customization Tips

* **Changing the time resolution**: In `planet.py`, update the `time_step` variable to speed up or slow down the simulation.
* **Plot appearance**: Customize Matplotlib settings (colors, markers, labels) inside `planet.py` to match your style.
* **Output format**: Modify `make_vid.sh` to change video codecs or output formats (e.g., GIF).

---

### Refrences 
- [NASA's JPL](https://ssd.jpl.nasa.gov/planets/approx_pos.html#tables)

### 📜 License

This project is released under the MIT License.
