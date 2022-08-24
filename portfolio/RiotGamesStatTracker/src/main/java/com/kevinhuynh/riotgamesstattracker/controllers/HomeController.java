package com.kevinhuynh.riotgamesstattracker.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

import com.kevinhuynh.riotgamesstattracker.models.Summoner;
import com.kevinhuynh.riotgamesstattracker.services.SummonerService;

@Controller
public class HomeController {
	
	@Autowired 
	private SummonerService summonerService;
	
	@GetMapping("/")
	public String index(Model model) {
		model.addAttribute("summoner", new Summoner());
		return "index.jsp";
	}
	
	@GetMapping("/dashboard")
	public String dashboard(Model model) {
		
		return "dashboard.jsp";
	}
	
	
	@PostMapping("/summoner")
	public String displaySummoner(@ModelAttribute("summoner") Summoner summoner, Model model) {
		System.out.println(summoner.getName());
		System.out.println(summonerService.getSummonerData(summoner.getName()));
		return "redirect:/dashboard.jsp";
	}
	
	
}
