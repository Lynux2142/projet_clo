/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   TNM.cpp                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lynux <marvin@42.fr>                       +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/20 13:32:07 by lynux             #+#    #+#             */
/*   Updated: 2022/01/20 15:40:26 by lynux            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <TNM.hpp>

void	SDL_ExitWithError(const char *message, const char *error) {
	SDL_Log("%s: %s\n", message, error);
	exit(1);
}

void	init(SDL_Window **window, SDL_Renderer **renderer, SDL_Surface **background, SDL_Surface **square, Mix_Music **sound) {
	if ((*window = SDL_CreateWindow("Test de la négligence sensorielle", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WINDOW_W, WINDOW_H, SDL_WINDOW_RESIZABLE)) == NULL)
		SDL_ExitWithError("Error Create window", SDL_GetError());
	if ((*renderer = SDL_CreateRenderer(*window, -1, 0)) == NULL)
		SDL_ExitWithError("Error Create renderer", SDL_GetError());
	if ((*background = SDL_CreateRGBSurface(0, WINDOW_W, WINDOW_H, 32, RMASK, GMASK, BMASK, AMASK)) == NULL)
		SDL_ExitWithError("Error Create background", SDL_GetError());
	if ((*square = SDL_CreateRGBSurface(0, RECT_SIZE, RECT_SIZE, 32, RMASK, GMASK, BMASK, AMASK)) == NULL)
		SDL_ExitWithError("Error Create square", SDL_GetError());
	if ((*sound = Mix_LoadMUS(MUSIC_PATH)) == NULL)
		SDL_ExitWithError("Error Load music", Mix_GetError());
}

void	draw_line(SDL_Renderer **renderer, SDL_Surface **background, SDL_MouseMotionEvent motion) {
	SDL_Texture	*texture = NULL;
	SDL_Rect	rect = {motion.x, motion.y, 1, 1};

	SDL_FillRect(*background, &rect, 0xffffffff);
	texture = SDL_CreateTextureFromSurface(*renderer, *background);
	SDL_RenderCopy(*renderer, texture, NULL, NULL);
	SDL_DestroyTexture(texture);
}

void	change_target_pos(SDL_Rect *target, std::time_t *timestamp, Mix_Music *sound) {
	*target = {rand() % (WINDOW_W - RECT_SIZE), rand() % (WINDOW_H - RECT_SIZE), RECT_SIZE, RECT_SIZE};
	*timestamp = time(nullptr);
	Mix_PlayMusic(sound, 1);
}

int		main(int ac, char **av) {
	SDL_Window		*window		= NULL;
	SDL_Renderer	*renderer	= NULL;
	SDL_Surface		*background	= NULL;
	SDL_Surface		*square		= NULL;
	SDL_Texture		*texture	= NULL;
	SDL_Event		event;
	SDL_Rect		target;
	Mix_Music		*sound;
	std::time_t		timestamp = time(nullptr);
//	SDL_DisplayMode	DM;
	bool			stop;

	srand(time(nullptr));
	if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO) != 0)
		SDL_ExitWithError("Error Initialisation SDL", SDL_GetError());
	if (Mix_OpenAudio(44100, MIX_DEFAULT_FORMAT, 2, 1024) != 0)
		SDL_ExitWithError("Error Open audio", Mix_GetError());
	init(&window, &renderer, &background, &square, &sound);
	SDL_FillRect(background, NULL, 0xff);
	texture = SDL_CreateTextureFromSurface(renderer, background);
	SDL_RenderCopy(renderer, texture, NULL, NULL);
	change_target_pos(&target, &timestamp, sound);
	while (!stop) {
		while (SDL_PollEvent(&event)) {
			if (event.type == SDL_QUIT || (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_ESCAPE))
				stop = true;
			if (event.type == SDL_MOUSEMOTION) {
				draw_line(&renderer, &background, event.motion);
				if (event.motion.x >= target.x && event.motion.y >= target.y &&
						event.motion.x <= target.x + target.w && event.motion.y <= target.y + target.h)
					change_target_pos(&target, &timestamp, sound);
			}
			if (event.type == SDL_KEYDOWN && event.key.keysym.sym == SDLK_SPACE) {
				IMG_SavePNG(background, "./output/out.png");
				stop = true;
			}
		}
		if (time(nullptr) - timestamp >= 5)
			change_target_pos(&target, &timestamp, sound);
		texture = SDL_CreateTextureFromSurface(renderer, background);
		SDL_RenderCopy(renderer, texture, NULL, NULL);
		SDL_DestroyTexture(texture);
		SDL_FillRect(square, NULL, 0xff0000ff);
		texture = SDL_CreateTextureFromSurface(renderer, square);
		SDL_RenderCopy(renderer, texture, NULL, &target);
		SDL_DestroyTexture(texture);
		SDL_RenderPresent(renderer);
	}
	SDL_DestroyWindow(window);
	SDL_Quit();
	return (0);
}
