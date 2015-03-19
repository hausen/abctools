% provaufabc.cls
% 2014-08-17 Rodrigo Hausen
\ProvidesClass{provaufabc}[2014/08/17 version 1.00 Prova UFABC]
\NeedsTeXFormat{LaTeX2e}

% decimal separator
\xdef\DECIMALSEP{,}

% space between questions
\def\question@spacing{1.5ex}

\newif\ifaddpoints
\addpointsfalse
\DeclareOption{addpoints}{
\addpointstrue
}

% inspired by:
% http://tutex.tug.org/pracjourn/2005-4/hefferon/hefferon.pdf
% http://latex-project.org/guides/clsguide.pdf


% --- Class structure: declaration of options part
% ---
% This class extends the article class

% Read all the documentclass options; pass them to article,
% unless the file "<currentoption>.min" exists, then it is loaded
\DeclareOption*{\InputIfFileExists{\CurrentOption.min}{}{%
\PassOptionsToClass{\CurrentOption}{article}}}

% --- Class structure: execution of options part
% ---
\ProcessOptions \relax

% --- Class structure: declaration of options part
% ---
\LoadClass{article}

\RequirePackage[T1]{fontenc}
\RequirePackage[portuguese,brazil]{babel}
\RequirePackage{setspace}
\RequirePackage[table]{xcolor}
\RequirePackage{tikz}
\RequirePackage{icomma}
\RequirePackage{ifthen}

\RequirePackage{helvet}
\RequirePackage{lmodern}
\RequirePackage{times}
\RequirePackage{mathptmx}

% Page layout
\RequirePackage[paper=a4paper,left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}

\fontsize{12}{14.4}
\selectfont

\@ifundefined{numprova}{%
\global\let\@numprova\@empty
}% else if defined \prova
{%
\global\let\@numprova\numprova
}

\newcommand{\numerodaprova}[1]{\def\@numprova{#1}}

\newlength{\@leftheader}
\setlength{\@leftheader}{3cm}
\newlength{\@rightheader}
\setlength{\@rightheader}{3cm}
\newlength{\@middleheader}
\setlength{\@middleheader}{\linewidth}
\addtolength{\@middleheader}{-\@leftheader}
\addtolength{\@middleheader}{-\@rightheader}

\def\makeheader{
\definecolor{ufabcgreen}{RGB}{0,0,0}
\definecolor{ufabcyellow}{RGB}{201,201,201}
%\definecolor{ufabcgreen}{RGB}{0,91,60}
%\definecolor{ufabcyellow}{RGB}{254,205,7}

\noindent
\begin{minipage}[t]{\@leftheader}
\vspace{-0.5cm}% hack to align minipages to the top when there exists an image
\resizebox{2.8cm}{!}{%
{% select helvetica
\fontfamily{phv}\fontencoding{T1}\fontsize{10pt}{12pt}\selectfont%
\begin{tikzpicture}[y=0.80pt,x=0.80pt,yscale=-1, inner sep=0pt, outer sep=0pt]
\begin{scope}[shift={(-179.61585,-554.96138)}]
  \begin{scope}[cm={{0.42273,0.0,0.0,0.42273,(103.68748,380.07152)}}]
    \path[fill=ufabcgreen] (280.0312,509.4688) .. controls (258.8530,518.1708) and
      (243.9375,538.9965) .. (243.9375,563.3125) .. controls (243.9375,595.4610) and
      (270.0077,621.5312) .. (302.1562,621.5312) .. controls (334.3048,621.5312) and
      (360.3750,595.4610) .. (360.3750,563.3125) .. controls (360.3750,560.6304) and
      (360.1951,557.9918) .. (359.8438,555.4062) -- (346.0000,547.4375) .. controls
      (347.7929,552.3891) and (348.7500,557.7421) .. (348.7500,563.3125) .. controls
      (348.7500,589.0454) and (327.8890,609.9062) .. (302.1562,609.9062) .. controls
      (276.4235,609.9062) and (255.5625,589.0454) .. (255.5625,563.3125) .. controls
      (255.5625,540.4004) and (272.1164,521.3699) .. (293.9062,517.4688) -- cycle;
    \path[fill=ufabcgreen] (406.9688,505.1250) .. controls (391.5986,505.1250) and
      (377.6252,511.0877) .. (367.2188,520.8125) -- (377.7500,527.0000) .. controls
      (385.7410,520.5609) and (395.9081,516.7188) .. (406.9688,516.7188) .. controls
      (409.6790,516.7188) and (412.3228,516.9621) .. (414.9062,517.4062) --
      (420.8438,506.8125) .. controls (416.3978,505.7265) and (411.7493,505.1250) ..
      (406.9688,505.1250) -- cycle(450.7188,524.9375) -- (444.1250,535.2188) ..
      controls (450.0441,543.0321) and (453.5625,552.7545) .. (453.5625,563.3125) ..
      controls (453.5625,589.0454) and (432.7015,609.9062) .. (406.9688,609.9062) ..
      controls (381.2360,609.9062) and (360.3750,589.0454) .. (360.3750,563.3125) ..
      controls (360.3750,560.4490) and (360.6304,557.6583) .. (361.1250,554.9375) ..
      controls (361.0375,555.2953) and (360.9580,555.6222) .. (360.8750,556.0000) --
      (350.3125,549.9062) .. controls (349.2944,554.2159) and (348.7500,558.6911) ..
      (348.7500,563.3125) .. controls (348.7500,595.4610) and (374.8202,621.5312) ..
      (406.9688,621.5312) .. controls (439.1173,621.5312) and (465.1875,595.4610) ..
      (465.1875,563.3125) .. controls (465.1875,548.6018) and (459.7208,535.1803) ..
      (450.7188,524.9375) -- cycle;
    \path[fill=ufabcgreen] (354.1875,413.7188) .. controls (322.0390,413.7188) and
      (295.9688,439.7577) .. (295.9688,471.9062) .. controls (295.9688,474.4389) and
      (296.1237,476.9276) .. (296.4375,479.3750) -- (310.2500,487.4375) .. controls
      (308.5328,482.5795) and (307.5938,477.3523) .. (307.5938,471.9062) .. controls
      (307.5938,446.1734) and (328.4547,425.3125) .. (354.1875,425.3125) .. controls
      (379.9203,425.3125) and (400.7812,446.1734) .. (400.7812,471.9062) .. controls
      (400.7812,494.9415) and (384.0573,514.0858) .. (362.0938,517.8438) --
      (375.9062,525.9062) .. controls (397.2924,517.2926) and (412.4062,496.3721) ..
      (412.4062,471.9062) .. controls (412.4062,439.7577) and (386.3360,413.7188) ..
      (354.1875,413.7188) -- cycle;
    \path[fill=ufabcyellow] (258.0940,475.8176) -- (361.6346,535.6692) .. controls
      (363.9916,537.1844) and (367.1063,537.1844) .. (369.4633,535.6692) .. controls
      (372.3096,531.9337) and (374.6564,529.6141) .. (377.7655,527.0039) --
      (252.0331,453.3417) .. controls (248.5003,459.5201) and (250.1854,467.2836) ..
      (258.0940,475.8176) -- cycle;
    \path[fill=ufabcyellow] (269.5845,503.4705) .. controls (271.1431,497.4019) and
      (269.7886,490.6397) .. (264.2812,482.8887) -- (360.2457,538.6996) .. controls
      (365.3806,544.9710) and (362.5606,548.3382) .. (360.8770,555.9985) -- cycle;
    \path[fill=ufabcgreen] (177.49776,658.04559) node[above right] (text3883)
      {\color{ufabcgreen}Universidade Federal do ABC};
  \end{scope}
\end{scope}

\end{tikzpicture}%
}% end select helvetica
}% end of resizebox
\end{minipage}%
\hfill%
\begin{minipage}[t]{\@middleheader}
\begin{center}
\@title\\[3pt]
\@date\\[3pt]
\@author
\end{center}
\end{minipage}%
\hfill%
\begin{minipage}[t]{\@rightheader}
\ifx\@numprova\@empty
	{\color{white}prova sem n\'umero}
\else
	\raggedleft
	N\'umero da Prova:\\[6pt]
	{% select helvetica
	\fontfamily{phv}\fontencoding{T1}\fontsize{30pt}{36pt}\fontseries{b}\selectfont%
	\@numprova
	}% end select helvetica
\fi %
\end{minipage}

\vspace{0.5cm}

\noindent
Nome: \hrulefill{ }RA: \rule{4cm}{0.4pt}

\vspace{1ex}

}% end of makeheader

\newlength{\@instructionsep}
\setlength{\@instructionsep}{0pt}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{instructions}%
{% first part of instructions environment

\@par
\noindent
\textbf{Antes de come\c{c}ar, leia as instru\c{c}\~oes abaixo.}

\vspace{-4pt}

\begin{itemize}
\setlength{\itemsep}{\@instructionsep}
}% end first part of instructions environment
{% last part of instructions environment
\end{itemize}
}% end last part of instructions environment

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{cheatsheet}%
{% first part of cheatsheet environment

\@par
\noindent
\textbf{Lembretes:}

\vspace{-10pt}

\begin{itemize}
\setlength{\itemsep}{\@instructionsep}
}% end first part of cheatsheet environment
{% last part of cheatsheet environment
\end{itemize}
}% end last part of cheatsheet environment

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% counters and macros for questions and subquestions
\newcounter{the@question}
\newcounter{the@subquestion}
\newdimen\TMPPOINTS
\global\newdimen\TOTALPOINTS
\def\ADDPOINTS#1{\global\advance \TOTALPOINTS by #1pt}
{\catcode`.=12 \catcode`p=12 \catcode`t=12 \gdef\REMOVEUNIT#1.#2pt{#1\DECIMALSEP#2}}
\gdef\PRINTPOINTS#1{\TMPPOINTS=#1pt\relax\expandafter\REMOVEUNIT\the\TMPPOINTS}
\def\questionpoints#1{\expandafter\REMOVEUNIT#1}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{question}[1][\@empty]%
{% first part of question environment

\@par
\noindent \setcounter{the@subquestion}{0}\stepcounter{the@question}%
\fbox{\textbf{Quest\~ao \arabic{the@question}}}{ }%
\def\@currentlabel{\arabic{the@question}}%
%
\ifx#1\@empty% if the number of points is not given
	\let\question@points\@empty%
\else% if given
	\def\question@points{#1}%
	\ADDPOINTS{#1}%
	{(\PRINTPOINTS{#1} pt){ }}%
\fi%
}% end first part of question environment
{% last part of question environment
\vspace{\question@spacing}%
}% end last part of question environment


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{subquestion}[1][\@empty] %
{% first part of subquestion environment

\@par
\stepcounter{the@subquestion}\textbf{(\alph{the@subquestion})}{ }%
\def\@currentlabel{\alph{the@subquestion}}%
\ifx#1\@empty% if the number of points is not given
\else% if given
	\ifx\question@points\@empty% if no points were given in
%                                    the parent question
		\def\question@points{#1}%
		\ADDPOINTS{#1}%
		{(\PRINTPOINTS{#1} pt){ }}%
	\else% if points were given to the parent question
		\PackageError{provaufabc}{%
			Error in question \arabic{the@question}.\MessageBreak%
			If you attribute points to a question,\MessageBreak%
			you must not attribute points to its subquestions.
		}%
	\fi%
\fi%
}% end first part of subquestion environment
{% last part of subquestion environment
}% end last part of subquestion environment


% \customlabel from: http://tex.stackexchange.com/questions/18191/defining-custom-labels
\makeatletter
\newcommand{\customlabel}[2]{%
\protected@write \@auxout {}{\string \newlabel {#1}{{#2}{\thepage}}}}
%\protected@write \@auxout {}{\string \newlabel {#1}{{#2}{\thepage}{#2}{#1}{}} }%
\makeatother

\AtEndDocument{
\ifaddpoints
	\customlabel{totalpoints}{\expandafter\REMOVEUNIT\the\TOTALPOINTS}
	\customlabel{totalquestions}{\arabic{the@question}}
\fi
}% end AtEndDocument
