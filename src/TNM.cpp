/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   TNM.cpp                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lynux <marvin@42.fr>                       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/20 13:32:07 by lynux             #+#    #+#             */
/*   Updated: 2022/01/20 18:44:35 by lynux            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <TNM.hpp>

void	SDL_ExitWithError(const char *message, const char *error) {
	SDL_Log("%s: %s\n", message, error);
	exit(1);
}

void	init(SDL_DisplayMode screen, SDL_Window **window, SDL_Renderer **renderer, SDL_Surface **background, SDL_Surface **square, Mix_Music **sound) {
	if ((*window = SDL_CreateWindow("Sensory Neglect Test", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, screen.w, screen.h, SDL_WINDOW_FULLSCREEN)) == NULL)
		SDL_ExitWithError("Error Create window", SDL_GetError());
	if ((*renderer = SDL_CreateRenderer(*window, -1, 0)) == NULL)
		SDL_ExitWithError("Error Create renderer", SDL_GetError());
	if ((*background = SDL_CreateRGBSurface(0, screen.w, screen.h, 32, RMASK, GMASK, BMASK, AMASK)) == NULL)
		SDL_ExitWithError("Error Create background", SDL_GetError());
	if ((*square = SDL_CreateRGBSurface(0, RECT_SIZE, RECT_SIZE, 32, RMASK, GMASK, BMASK, AMASK)) == NULL)
		SDL_ExitWithError("Error Create square", SDL_GetError());
	if ((*sound = Mix_LoadMUS(MUSIC_PATH)) == NULL)
		SDL_ExitWithError("Error Load music", Mix_GetError());
}

void	print_surface(SDL_Renderer **renderer, SDL_Surface *surface, SDL_Rect *dest) {
	SDL_Texture	*texture = NULL;

	if ((texture = SDL_CreateTextureFromSurface(*renderer, surface)) == NULL)
		SDL_ExitWithError("Error Create texture", SDL_GetError());
	SDL_RenderCopy(*renderer, texture, NULL, dest);
	SDL_DestroyTexture(texture);
}

void	putpixel(SDL_Surface **background, int x, int y) {
	Uint8		*pixels = (Uint8*)(*background)->pixels;
	int			i;

	i = x * (Uint32)(*background)->format->BytesPerPixel + y * (*background)->pitch;
	pixels[i] = 0xff;
	pixels[i + 1] = 0xff;
	pixels[i + 2] = 0xff;
	pixels[i + 3] = 0xff;
}

void draw_line(SDL_Surface **background, int x0, int y0, int x1, int y1) {
	int dx = std::abs(x1 - x0);
	int sx = (x0 < x1 ? 1 : -1);
	int dy = -std::abs(y1 - y0);
	int sy = (y0 < y1 ? 1 : -1);
	int err = dx + dy;
	int e2;

	while (true) {
		putpixel(background, x0, y0);
		if (x0 == x1 && y0 == y1)
			break;
		e2 = 2 * err;
		if (e2 >= dy) {
			err += dy;
			x0 += sx;
		}
		if (e2 <= dx) {
			err += dx;
			y0 += sy;
		}
	}
}

void	change_target_pos(SDL_DisplayMode screen, SDL_Rect *target, std::time_t *timestamp, Mix_Music *sound) {
	*target = {rand() % (screen.w - RECT_SIZE), rand() % (screen.h - RECT_SIZE), RECT_SIZE, RECT_SIZE};
	*timestamp = time(nullptr);
	Mix_PlayMusic(sound, 1);
}

int		main(int ac, char **av) {
	SDL_Window		*window		= NULL;
	SDL_Renderer	*renderer	= NULL;
	SDL_Surface		*background	= NULL;
	SDL_Surface		*square		= NULL;
	Mix_Music		*sound		= NULL;
	SDL_DisplayMode	screen;
	SDL_Event		event;
	SDL_Rect		target;
	std::time_t		timestamp = time(nullptr);
	bool			stop;

	srand(time(nullptr));
	if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO) != 0)
		SDL_ExitWithError("Error Initialisation SDL", SDL_GetError());
	if (Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 1024) != 0)
		SDL_ExitWithError("Error Open audio", Mix_GetError());
	SDL_GetCurrentDisplayMode(0, &screen);
	init(screen, &window, &renderer, &background, &square, &sound);
	SDL_FillRect(background, NULL, BLACK);
	change_target_pos(screen, &target, &timestamp, sound);
	while (!stop) {
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT || (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE))
				stop = true;
			if (event.type == SDL_MOUSEMOTION) {
				draw_line(&background, event.motion.x - event.motion.xrel, event.motion.y - event.motion.yrel, event.motion.x, event.motion.y);
				if (event.motion.x >= target.x && event.motion.y >= target.y &&
						event.motion.x <= target.x + target.w && event.motion.y <= target.y + target.h)
					change_target_pos(screen, &target, &timestamp, sound);
			}
			if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_SPACE) {
				std::filesystem::create_directory("./output");
				SDL_SaveBMP(background, "./output/out.bmp");
				stop = true;
			}
		}
		if (time(nullptr) - timestamp >= TIME_BEFORE_CHANGE)
			change_target_pos(screen, &target, &timestamp, sound);
		print_surface(&renderer, background, NULL);
		SDL_FillRect(square, NULL, RED);
		print_surface(&renderer, square, &target);
		SDL_RenderPresent(renderer);
	}
	SDL_FreeSurface(square);
	SDL_FreeSurface(background);
	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);
	Mix_FreeMusic(sound);
	SDL_Quit();
	return (0);
}
