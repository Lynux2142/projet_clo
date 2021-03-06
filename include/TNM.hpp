/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   TNM.hpp                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: lguiller <lguiller@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2022/01/21 11:50:47 by lguiller          #+#    #+#             */
/*   Updated: 2022/01/24 15:31:19 by lguiller         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef TNM_HPP
# define TNM_HPP

# include <SDL2/SDL.h>
# include <SDL2/SDL_mixer.h>
# include <iostream>
# include <ctime>
# include <filesystem>

# define MUSIC_PATH			"./sounds/clearly.ogg"
# define RECT_SIZE			20
# define TIME_BEFORE_CHANGE	5
# define RMASK				0xff000000
# define GMASK				0xff0000
# define BMASK				0xff00
# define AMASK				0xff
# define WHITE				0xffffffff
# define BLACK				0xff
# define RED				0xff0000ff
# define BACKGROUND_COLOR	BLACK
# define SQUARE_COLOR		RED
# define TRAIL_COLOR		WHITE

#endif
