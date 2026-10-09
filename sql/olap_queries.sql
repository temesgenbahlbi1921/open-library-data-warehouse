========================================================================================================================================
								FINAL SQL CODES FOR OLAP
								       OLAP OPERATIONS  
									   1 ROLL UP
									   2 DRILL DOWN
									   3 SLICE
									   4 DICE
									   5 PIVOT 
========================================================================================================================================
 
1. Roll-Up: Aggregating data from detailed to summary level (Year-wise book count)
		Reduces the detail level of the data by aggregating it along a dimension.
		Example: Summarizing sales data yearly.

					SELECT EXTRACT(YEAR FROM publish_date) AS year, COUNT(*) AS published_books
					FROM dim_editions
					WHERE publish_date IS NOT NULL
					GROUP BY year
					ORDER BY year;




2. Drill-Down: Breaking down data to finer levels
 		Increases the detail level of the data by breaking down aggregated data into finer granularity.
		Example:Drill down from year to month for book count
		
						SELECT 
								  EXTRACT(YEAR FROM publish_date) AS year,
								  EXTRACT(MONTH FROM publish_date) AS month,
								  COUNT(*) AS published_books
						FROM dim_editions
						WHERE publish_date IS NOT NULL
						GROUP BY year, month
						ORDER BY year, month;



		Example 2:Drill down to individual books in the year 2020 month 5
					  SELECT title, publish_date
					  FROM dim_editions
					  WHERE EXTRACT(YEAR FROM publish_date) = 2020
					  AND EXTRACT(MONTH FROM publish_date) = 5
					  ORDER BY publish_date;


3. Slice:
		Filtering data on one dimension
		Ex :Slice by specific year (e.g., 2018)
		
					SELECT book_id,title,authors,publish_date,publishers
					FROM dim_editions
					WHERE EXTRACT(YEAR FROM publish_date) = 2018
					ORDER BY book_id;

					

 		Ex 2:Slice by physical format = 'Hardcover'
		 
					SELECT  book_id,title,authors,publishers,physical_format
					FROM dim_editions
					WHERE physical_format = 'Hardcover'
					ORDER BY book_id;




					
4. Dice: Filtering data on multiple dimensions
		Dice where year is between 2010–2020 AND format is 'Paperback'
		
					SELECT book_id,title,revision,authors,publishers,publish_date,physical_format
					FROM dim_editions
					WHERE EXTRACT(YEAR FROM publish_date) BETWEEN 2000 AND 2022
					AND physical_format = 'Paperback'
					ORDER BY publish_date;

					
 5. Pivot: Converting rows to columns for conveying insights and analysis 
			 => Counting  rating of book per rating values across rating values as columns
			
					SELECT 
					    dim_ratings.book_id,
					    dim_editions.title,
					    COUNT(*) FILTER (WHERE dim_ratings.rating = 1) AS "Rating=1",
					    COUNT(*) FILTER (WHERE dim_ratings.rating = 2) AS "Rating=2",
					    COUNT(*) FILTER (WHERE dim_ratings.rating = 3) AS "Rating=3",
					    COUNT(*) FILTER (WHERE dim_ratings.rating = 4) AS "Rating=4",
					    COUNT(*) FILTER (WHERE dim_ratings.rating = 5) AS "Rating=5"
					FROM dim_ratings
					JOIN dim_editions ON dim_ratings.book_id = dim_editions.book_id
					GROUP BY dim_ratings.book_id, dim_editions.title
					ORDER BY dim_ratings.book_id;
=================================================================================================================================================
													Aggregation 
													1 COUNT
													2 SUM
													3 AVG
													
=================================================================================================================================================
1 To count how many books were published in each year, based on the publish_date:

				SELECT 
						EXTRACT(YEAR FROM publish_date) AS publish_year, COUNT(*) AS books_per_year
						FROM dim_editions
						GROUP BY publish_year
				ORDER BY publish_year;

2) To calculate the sum of ratings for each book:

				SELECT dim_editions.book_id, dim_editions.title, SUM(dim_ratings.rating) AS total_rating
				FROM dim_ratings
				JOIN dim_editions ON dim_ratings.book_id = dim_editions.book_id
				GROUP BY dim_editions.book_id, dim_editions.title
				ORDER BY total_rating DESC;

				
3) Average Number of Books Published per Year from 2010 to 2022
===================================================================
SELECT 
    Publication_year,
    Total_books,
    AVG(total_books) OVER () AS Average_published_book
FROM (
        SELECT 
        EXTRACT(YEAR FROM publish_date) AS Publication_year,
        COUNT(DISTINCT book_id) AS Total_books
	    FROM dim_editions
	    WHERE EXTRACT(YEAR FROM publish_date) BETWEEN 2010 AND 2022
	    GROUP BY EXTRACT(YEAR FROM publish_date)
	    ORDER BY publication_year
   )
ORDER BY publication_year;


=====================================================================================================
					Filtering Using WHERE 
=====================================================================================================
	1) selecting  books published after 2015
				SELECT 
					    book_id,
					    title,
					    publish_date
					FROM dim_editions
					WHERE EXTRACT(YEAR FROM publish_date) > 2015;

	2) selecting  ratings thier rating value is 1,4,5 			
				SELECT *
					FROM dim_ratings 
					WHERE rating > 3 or rating < 2
					ORDER BY rating;
===============================================================================================================================
						        SIMPLE JOIN     
								SIMPLE JOIN     
								SIMPLE JOIN       
								SIMPLE JOIN
===============================================================================================================================
1: JOIN uses to Filtering Books Published After 2000 with Ratings
				SELECT 
				    de.book_id,
				    de.title,
				    dr.rating
				FROM dim_editions de
				JOIN dim_ratings dr ON de.book_id = dr.book_id
				WHERE EXTRACT(YEAR FROM de.publish_date) > 2000;

2) : JOIN to detect book with its author id and name the rating value

		SELECT DISTINCT dim_ratings.book_id,dim_editions.title,  dim_authors.author_id, dim_authors.name,dim_ratings.rating 
		FROM dim_works
		JOIN dim_authors ON dim_authors.author_id = dim_works.authors
		JOIN dim_ratings ON dim_works.work_id = dim_ratings.work_id
		JOIN dim_editions ON dim_editions.authors = dim_authors.author_id;