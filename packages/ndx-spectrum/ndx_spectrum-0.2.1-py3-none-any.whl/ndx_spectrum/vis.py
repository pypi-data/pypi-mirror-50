import matplotlib.pyplot as plt


def show_spectrum(spectrum):
    naxes = 0
    if 'power' in spectrum:
        naxes += 1
    if 'phase' in spectrum:
        naxes += 1

    fig, axs = plt.subplots(naxes, 1, sharex=True)

    caxes = 0
    ax = axs[caxes]
    if 'power' in spectrum:
        ax.semilogy(spectrum.frequencies, spectrum.power)
        ax.set_ylabel('Power')

        caxes += 1

    if 'phase' in spectrum:
        ax.plot(spectrum.frequencies, spectrum.phase)
        ax.set_ylabel('phase')

    ax.set_xlabel('frequency')

    return fig

