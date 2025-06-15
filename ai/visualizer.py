import pygame
import numpy as np

class SimpleNetVisualizer:
    def __init__(self, surface, position, size):
        self.surface = surface
        self.position = position
        self.size = size

        self.neuron_radius = 10
        self.spacing_x = 120
        self.spacing_y = 25
        self.max_visible_neurons = 5# Solo muestra hasta 10 neuronas por capa

    def draw_network(self, individual, input_vector):
        self.surface.fill((30, 30, 30))  # Fondo oscuro

        layers = individual.get_activations(input_vector)
        layers = [input_vector] + layers  # Agrega entrada como capa 0

        num_layers = len(layers)
        layer_positions = []

        for i, layer in enumerate(layers):
            n_neurons = len(layer)

            if n_neurons > self.max_visible_neurons:
                indices_to_show = np.linspace(0, n_neurons - 1, self.max_visible_neurons, dtype=int)
                show_ellipsis = True
            else:
                indices_to_show = range(n_neurons)
                show_ellipsis = False

            layer_pos = []
            total_height = len(indices_to_show) * self.spacing_y
            start_y = self.position[1] + (self.size[1] - total_height) // 2
            x = self.position[0] + i * self.spacing_x

            for j, idx in enumerate(indices_to_show):
                y = start_y + j * self.spacing_y
                layer_pos.append((x, y))

            if show_ellipsis:
                # Añade una posición central para los puntos suspensivos
                ellipsis_y = start_y + len(indices_to_show) * self.spacing_y + 5
                layer_pos.append((x, ellipsis_y))

            layer_positions.append(layer_pos)

        # Dibujar conexiones
        for l in range(len(layer_positions) - 1):
            for i, src_pos in enumerate(layer_positions[l]):
                if i == self.max_visible_neurons:
                    continue  # No conectar puntos suspensivos
                for j, dst_pos in enumerate(layer_positions[l + 1]):
                    if j == self.max_visible_neurons:
                        continue
                    pygame.draw.line(self.surface, (100, 100, 100), src_pos, dst_pos, 1)

        # Dibujar neuronas
        for layer_idx, layer in enumerate(layers):
            n_neurons = len(layer)

            if n_neurons > self.max_visible_neurons:
                indices_to_show = np.linspace(0, n_neurons - 1, self.max_visible_neurons, dtype=int)
                show_ellipsis = True
            else:
                indices_to_show = range(n_neurons)
                show_ellipsis = False

            for j, idx in enumerate(indices_to_show):
                value = layer[idx]
                x, y = layer_positions[layer_idx][j]

                # Color según activación
                color_intensity = int(255 * min(1.0, abs(value)))
                if value >= 0:
                    g = min(255, 50 + color_intensity)
                    color = (255, g, 50)
                else:
                    b = min(255, 50 + color_intensity)
                    color = (50, 50, b)

                pygame.draw.circle(self.surface, color, (x, y), self.neuron_radius)

            # Dibujar puntos suspensivos si hay más neuronas ocultas
            if show_ellipsis:
                x, y = layer_positions[layer_idx][-1]
                font = pygame.font.SysFont("arial", 16)
                text_surface = font.render("...", True, (200, 200, 200))
                self.surface.blit(text_surface, (x - 10, y))

        pygame.display.update()
